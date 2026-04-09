from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.document_types.models import DocumentType
from apps.organizations.models import Organization
from apps.vendors.models import Vendor

from .enums import DocumentVerificationStatus
from .models import VendorDocument


def validate_document_ownership(*, document=None, vendor: Vendor | None = None, document_type: DocumentType | None = None, organization: Organization):
    if document is not None and document.organization_id != organization.id:
        raise ValidationError('Document does not belong to this organization.')
    if vendor is not None and vendor.organization_id != organization.id:
        raise ValidationError('Vendor does not belong to this organization.')
    if document_type is not None and document_type.organization_id != organization.id:
        raise ValidationError('Document type does not belong to this organization.')


def validate_file_extension(*, document_type: DocumentType, file_name: str) -> None:
    if not document_type.allowed_extensions:
        return
    ext = file_name.split('.')[-1].lower()
    allowed = [e.lower().lstrip('.') for e in document_type.allowed_extensions]
    if ext not in allowed:
        raise ValidationError('Invalid file extension.')


def validate_file_size(*, document_type: DocumentType, file_obj) -> None:
    max_bytes = int(document_type.max_file_size_mb) * 1024 * 1024
    if file_obj.size > max_bytes:
        raise ValidationError('File exceeds maximum size.')


def validate_expiry_required(*, document_type: DocumentType, expiry_date) -> None:
    if document_type.has_expiry and not expiry_date:
        raise ValidationError('Expiry date is required for this document type.')


def validate_status_transition(*, document: VendorDocument, to_status: str) -> None:
    current = document.verification_status
    allowed = {
        DocumentVerificationStatus.PENDING: {
            DocumentVerificationStatus.UNDER_REVIEW,
            DocumentVerificationStatus.APPROVED,
            DocumentVerificationStatus.REJECTED,
        },
        DocumentVerificationStatus.UNDER_REVIEW: {
            DocumentVerificationStatus.APPROVED,
            DocumentVerificationStatus.REJECTED,
        },
        DocumentVerificationStatus.APPROVED: set(),
        DocumentVerificationStatus.REJECTED: set(),
        DocumentVerificationStatus.EXPIRED: set(),
        DocumentVerificationStatus.SUPERSEDED: set(),
    }
    if to_status not in allowed.get(current, set()):
        raise ValidationError('Invalid status transition.')