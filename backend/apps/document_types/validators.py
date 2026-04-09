from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.organizations.models import Organization

from .models import DocumentType


def validate_document_type_ownership(*, document_type: DocumentType, organization: Organization) -> None:
    if document_type.organization_id != organization.id:
        raise ValidationError('Document type does not belong to this organization.')