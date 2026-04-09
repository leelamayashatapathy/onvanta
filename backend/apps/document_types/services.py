from __future__ import annotations

from apps.organizations.models import Organization

from .models import DocumentType
from .validators import validate_document_type_ownership


class DocumentTypeService:
    @staticmethod
    def create_document_type(*, organization: Organization, **data) -> DocumentType:
        return DocumentType.objects.create(organization=organization, **data)

    @staticmethod
    def update_document_type(*, document_type: DocumentType, organization: Organization, **data) -> DocumentType:
        validate_document_type_ownership(document_type=document_type, organization=organization)
        for field, value in data.items():
            setattr(document_type, field, value)
        document_type.save(update_fields=list(data.keys()) + ['updated_at'])
        return document_type