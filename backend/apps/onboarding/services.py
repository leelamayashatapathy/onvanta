from __future__ import annotations

from django.utils import timezone

from apps.auditlog.services import AuditService
from apps.document_types.models import DocumentType
from apps.organizations.models import Organization
from apps.vendors.enums import VendorOnboardingStatus
from apps.vendors.models import Vendor

from .enums import OnboardingCaseStatus, OnboardingRequirementStatus
from .models import (
    OnboardingCase,
    OnboardingRequirement,
    OnboardingTemplate,
    OnboardingTemplateRequirement,
)
from .validators import validate_template_ownership, validate_vendor_ownership


class OnboardingTemplateService:
    @staticmethod
    def create_template(*, organization: Organization, **data) -> OnboardingTemplate:
        return OnboardingTemplate.objects.create(organization=organization, **data)

    @staticmethod
    def update_template(
        *, template: OnboardingTemplate, organization: Organization, **data
    ) -> OnboardingTemplate:
        validate_template_ownership(template=template, organization=organization)
        for field, value in data.items():
            setattr(template, field, value)
        template.save(update_fields=list(data.keys()) + ['updated_at'])
        return template

    @staticmethod
    def add_requirement(
        *,
        template: OnboardingTemplate,
        document_type: DocumentType,
        required: bool,
        sequence: int,
        review_required: bool,
    ) -> OnboardingTemplateRequirement:
        return OnboardingTemplateRequirement.objects.create(
            template=template,
            document_type=document_type,
            required=required,
            sequence=sequence,
            review_required=review_required,
        )


class OnboardingService:
    @staticmethod
    def start_case(
        *, organization: Organization, vendor: Vendor, template: OnboardingTemplate, actor
    ) -> OnboardingCase:
        validate_vendor_ownership(vendor=vendor, organization=organization)
        validate_template_ownership(template=template, organization=organization)

        case = OnboardingCase.objects.create(
            organization=organization,
            vendor=vendor,
            template=template,
            status=OnboardingCaseStatus.COLLECTING_DOCUMENTS,
            current_stage='document_collection',
            started_at=timezone.now(),
        )
        OnboardingService.generate_requirements(case=case)
        OnboardingService.recalculate_progress(case=case)

        vendor.onboarding_status = VendorOnboardingStatus.DOCUMENTS_PENDING
        vendor.save(update_fields=['onboarding_status', 'updated_at'])

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='OnboardingCase',
            entity_id=case.id,
            action='onboarding_started',
            source='api',
            new_data={'vendor_id': str(vendor.id), 'case_id': str(case.id)},
        )
        return case

    @staticmethod
    def generate_requirements(*, case: OnboardingCase) -> None:
        template_requirements = case.template.requirements.select_related('document_type').order_by('sequence')
        bulk = []
        for req in template_requirements:
            bulk.append(
                OnboardingRequirement(
                    case=case,
                    document_type=req.document_type,
                    required=req.required,
                    status=OnboardingRequirementStatus.PENDING,
                )
            )
        OnboardingRequirement.objects.bulk_create(bulk)

    @staticmethod
    def recalculate_progress(*, case: OnboardingCase) -> None:
        total = case.requirements.count()
        if total == 0:
            case.progress_percent = 0
        else:
            verified_count = case.requirements.filter(verified=True).count()
            case.progress_percent = int((verified_count / total) * 100)
        case.save(update_fields=['progress_percent', 'updated_at'])

    @staticmethod
    def submit_for_review(*, case: OnboardingCase, organization: Organization, actor) -> OnboardingCase:
        required_requirements = case.requirements.filter(required=True)
        if required_requirements.filter(submitted=False).exists():
            case.blocked_reason = 'Required documents missing.'
            case.save(update_fields=['blocked_reason', 'updated_at'])
            return case

        case.status = OnboardingCaseStatus.UNDER_REVIEW
        case.current_stage = 'review'
        case.submitted_at = timezone.now()
        case.blocked_reason = ''
        case.save(update_fields=['status', 'current_stage', 'submitted_at', 'blocked_reason', 'updated_at'])

        case.vendor.onboarding_status = VendorOnboardingStatus.UNDER_REVIEW
        case.vendor.save(update_fields=['onboarding_status', 'updated_at'])

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='OnboardingCase',
            entity_id=case.id,
            action='onboarding_submitted',
            source='api',
            new_data={'case_id': str(case.id), 'vendor_id': str(case.vendor_id)},
        )
        return case

    @staticmethod
    def submit_for_approval(*, case: OnboardingCase, organization: Organization, actor) -> OnboardingCase:
        required_requirements = case.requirements.filter(required=True)
        if required_requirements.filter(verified=False).exists():
            case.blocked_reason = 'Required documents not verified.'
            case.save(update_fields=['blocked_reason', 'updated_at'])
            return case

        case.status = OnboardingCaseStatus.APPROVAL_PENDING
        case.current_stage = 'approval'
        case.blocked_reason = ''
        case.save(update_fields=['status', 'current_stage', 'blocked_reason', 'updated_at'])

        case.vendor.onboarding_status = VendorOnboardingStatus.APPROVAL_PENDING
        case.vendor.save(update_fields=['onboarding_status', 'updated_at'])

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='OnboardingCase',
            entity_id=case.id,
            action='onboarding_approval_submitted',
            source='api',
            new_data={'case_id': str(case.id), 'vendor_id': str(case.vendor_id)},
        )
        return case
