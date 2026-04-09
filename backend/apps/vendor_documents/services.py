from __future__ import annotations

import hashlib

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.auditlog.services import AuditService
from apps.document_types.models import DocumentType
from apps.onboarding.enums import OnboardingCaseStatus, OnboardingRequirementStatus
from apps.onboarding.models import OnboardingRequirement
from apps.onboarding.services import OnboardingService
from apps.organizations.models import Organization
from apps.vendors.models import Vendor

from .enums import DocumentStatus, DocumentVerificationStatus
from .models import VendorDocument
from .validators import (
    validate_document_ownership,
    validate_expiry_required,
    validate_file_extension,
    validate_file_size,
    validate_status_transition,
)


class DocumentService:
    @staticmethod
    def calculate_checksum(file_obj) -> str:
        hasher = hashlib.sha256()
        for chunk in file_obj.chunks():
            hasher.update(chunk)
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
        return hasher.hexdigest()

    @staticmethod
    def _get_active_requirement(*, vendor: Vendor, document_type: DocumentType) -> OnboardingRequirement | None:
        return (
            OnboardingRequirement.objects.select_related('case')
            .filter(case__vendor=vendor)
            .exclude(case__status__in=[OnboardingCaseStatus.CANCELLED, OnboardingCaseStatus.COMPLETED])
            .filter(document_type=document_type)
            .order_by('-case__created_at')
            .first()
        )

    @staticmethod
    def upload_document(
        *,
        organization: Organization,
        vendor: Vendor,
        document_type: DocumentType,
        file_obj,
        issue_date,
        expiry_date,
        uploaded_by,
    ) -> VendorDocument:
        validate_document_ownership(vendor=vendor, organization=organization)
        validate_document_ownership(document_type=document_type, organization=organization)
        validate_file_extension(document_type=document_type, file_name=file_obj.name)
        validate_file_size(document_type=document_type, file_obj=file_obj)
        validate_expiry_required(document_type=document_type, expiry_date=expiry_date)

        checksum = DocumentService.calculate_checksum(file_obj)
        vendor_document = VendorDocument.objects.create(
            organization=organization,
            vendor=vendor,
            document_type=document_type,
            file=file_obj,
            file_path='',
            original_name=file_obj.name,
            mime_type=getattr(file_obj, 'content_type', ''),
            file_size=file_obj.size,
            checksum=checksum,
            issue_date=issue_date,
            expiry_date=expiry_date,
            status=DocumentStatus.PENDING,
            verification_status=DocumentVerificationStatus.PENDING,
            uploaded_by=uploaded_by,
        )
        vendor_document.file_path = vendor_document.file.name
        vendor_document.save(update_fields=['file_path'])

        requirement = DocumentService._get_active_requirement(vendor=vendor, document_type=document_type)
        if requirement:
            requirement.submitted = True
            requirement.current_document = vendor_document
            requirement.status = OnboardingRequirementStatus.SUBMITTED
            requirement.save(update_fields=['submitted', 'current_document', 'status', 'updated_at'])

        AuditService.log_event(
            organization=organization,
            actor_user=uploaded_by,
            actor_type='user',
            entity_type='VendorDocument',
            entity_id=vendor_document.id,
            action='document_uploaded',
            source='api',
            new_data={
                'vendor_id': str(vendor.id),
                'document_type_id': str(document_type.id),
                'document_id': str(vendor_document.id),
            },
        )
        return vendor_document

    @staticmethod
    def mark_under_review(*, document: VendorDocument, organization: Organization, actor) -> VendorDocument:
        validate_document_ownership(document=document, organization=organization)
        validate_status_transition(document=document, to_status=DocumentVerificationStatus.UNDER_REVIEW)
        document.verification_status = DocumentVerificationStatus.UNDER_REVIEW
        document.verified_by = actor
        document.verified_at = timezone.now()
        document.save(update_fields=['verification_status', 'verified_by', 'verified_at', 'updated_at'])
        return document

    @staticmethod
    def approve_document(*, document: VendorDocument, organization: Organization, actor) -> VendorDocument:
        validate_document_ownership(document=document, organization=organization)
        validate_status_transition(document=document, to_status=DocumentVerificationStatus.APPROVED)
        document.verification_status = DocumentVerificationStatus.APPROVED
        document.status = DocumentStatus.ACTIVE
        document.verified_by = actor
        document.verified_at = timezone.now()
        document.rejection_reason = ''
        document.save(
            update_fields=[
                'verification_status',
                'status',
                'verified_by',
                'verified_at',
                'rejection_reason',
                'updated_at',
            ]
        )

        requirement = DocumentService._get_active_requirement(
            vendor=document.vendor, document_type=document.document_type
        )
        if requirement:
            requirement.submitted = True
            requirement.verified = True
            requirement.status = OnboardingRequirementStatus.VERIFIED
            requirement.current_document = document
            requirement.save(update_fields=['submitted', 'verified', 'status', 'current_document', 'updated_at'])
            OnboardingService.recalculate_progress(case=requirement.case)

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='VendorDocument',
            entity_id=document.id,
            action='document_approved',
            source='api',
            new_data={
                'document_id': str(document.id),
                'vendor_id': str(document.vendor_id),
                'document_type_id': str(document.document_type_id),
            },
        )
        return document

    @staticmethod
    def reject_document(
        *, document: VendorDocument, organization: Organization, actor, rejection_reason: str
    ) -> VendorDocument:
        validate_document_ownership(document=document, organization=organization)
        validate_status_transition(document=document, to_status=DocumentVerificationStatus.REJECTED)
        if not rejection_reason:
            raise ValidationError('Rejection reason is required.')
        document.verification_status = DocumentVerificationStatus.REJECTED
        document.status = DocumentStatus.REJECTED
        document.verified_by = actor
        document.verified_at = timezone.now()
        document.rejection_reason = rejection_reason
        document.save(
            update_fields=[
                'verification_status',
                'status',
                'verified_by',
                'verified_at',
                'rejection_reason',
                'updated_at',
            ]
        )

        requirement = DocumentService._get_active_requirement(
            vendor=document.vendor, document_type=document.document_type
        )
        if requirement:
            requirement.submitted = True
            requirement.verified = False
            requirement.status = OnboardingRequirementStatus.REJECTED
            requirement.current_document = document
            requirement.save(update_fields=['submitted', 'verified', 'status', 'current_document', 'updated_at'])
            OnboardingService.recalculate_progress(case=requirement.case)

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='VendorDocument',
            entity_id=document.id,
            action='document_rejected',
            source='api',
            new_data={
                'document_id': str(document.id),
                'vendor_id': str(document.vendor_id),
                'document_type_id': str(document.document_type_id),
                'reason': rejection_reason,
            },
        )
        return document