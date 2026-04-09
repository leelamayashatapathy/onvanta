from __future__ import annotations

from datetime import date, timedelta

from apps.organizations.models import Organization
from apps.vendor_documents.enums import DocumentStatus
from apps.vendor_documents.models import VendorDocument


def list_upcoming_expiries(*, organization: Organization, days: int = 30):
    return VendorDocument.objects.filter(
        organization=organization,
        expiry_date__isnull=False,
        expiry_date__gte=date.today(),
        expiry_date__lte=date.today() + timedelta(days=days),
        status=DocumentStatus.ACTIVE,
    ).select_related('vendor', 'document_type')


def list_overdue_expiries(*, organization: Organization):
    return VendorDocument.objects.filter(
        organization=organization,
        expiry_date__isnull=False,
        expiry_date__lt=date.today(),
        status=DocumentStatus.ACTIVE,
    ).select_related('vendor', 'document_type')
