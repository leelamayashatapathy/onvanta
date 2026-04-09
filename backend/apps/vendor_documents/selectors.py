from __future__ import annotations

from django.db.models import QuerySet

from apps.organizations.models import Organization

from .models import VendorDocument


def list_vendor_documents(*, organization: Organization, vendor_id) -> QuerySet[VendorDocument]:
    return (
        VendorDocument.objects.filter(organization=organization, vendor_id=vendor_id)
        .select_related('vendor', 'document_type', 'uploaded_by')
        .order_by('-created_at')
    )


def get_document_detail(*, organization: Organization, document_id) -> VendorDocument:
    return VendorDocument.objects.select_related('vendor', 'document_type', 'uploaded_by').get(
        id=document_id, organization=organization
    )