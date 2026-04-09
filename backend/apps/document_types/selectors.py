from __future__ import annotations

from django.db.models import QuerySet

from apps.organizations.models import Organization

from .models import DocumentType


def list_document_types(*, organization: Organization) -> QuerySet[DocumentType]:
    return DocumentType.objects.filter(organization=organization).order_by('name')


def get_document_type_detail(*, organization: Organization, document_type_id) -> DocumentType:
    return DocumentType.objects.get(id=document_type_id, organization=organization)