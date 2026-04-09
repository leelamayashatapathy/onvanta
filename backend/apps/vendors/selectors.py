from __future__ import annotations

from django.db.models import QuerySet

from apps.organizations.models import Organization
from apps.auditlog.selectors import list_vendor_related_events
from apps.vendor_documents.models import VendorDocument
from apps.vendor_documents.enums import DocumentVerificationStatus

from .models import Vendor


def list_vendors(*, organization: Organization) -> QuerySet[Vendor]:
    return (
        Vendor.objects.filter(organization=organization)
        .select_related('owner_user', 'organization')
        .order_by('display_name')
    )


def get_vendor_detail(*, organization: Organization, vendor_id) -> Vendor:
    return Vendor.objects.select_related('owner_user', 'organization').get(
        id=vendor_id, organization=organization
    )


def get_vendor_timeline(*, organization: Organization, vendor_id):
    return list_vendor_related_events(organization=organization, vendor_id=vendor_id)


def get_vendor_status_summary(*, organization: Organization, vendor_id) -> dict:
    total_docs = VendorDocument.objects.filter(organization=organization, vendor_id=vendor_id).count()
    pending = VendorDocument.objects.filter(
        organization=organization,
        vendor_id=vendor_id,
        verification_status=DocumentVerificationStatus.PENDING,
    ).count()
    approved = VendorDocument.objects.filter(
        organization=organization,
        vendor_id=vendor_id,
        verification_status=DocumentVerificationStatus.APPROVED,
    ).count()
    rejected = VendorDocument.objects.filter(
        organization=organization,
        vendor_id=vendor_id,
        verification_status=DocumentVerificationStatus.REJECTED,
    ).count()
    expired = VendorDocument.objects.filter(
        organization=organization,
        vendor_id=vendor_id,
        verification_status=DocumentVerificationStatus.EXPIRED,
    ).count()
    return {
        'total_documents': total_docs,
        'pending_verification': pending,
        'approved': approved,
        'rejected': rejected,
        'expired': expired,
    }
