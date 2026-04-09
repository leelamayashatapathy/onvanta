from __future__ import annotations

from django.db.models import QuerySet

from apps.organizations.models import Organization

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