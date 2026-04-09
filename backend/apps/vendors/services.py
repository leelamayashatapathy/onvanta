from __future__ import annotations

from apps.organizations.models import Organization

from .models import Vendor
from .validators import validate_vendor_ownership


class VendorService:
    @staticmethod
    def create_vendor(*, organization: Organization, **data) -> Vendor:
        vendor = Vendor.objects.create(organization=organization, **data)
        return vendor

    @staticmethod
    def update_vendor(*, vendor: Vendor, organization: Organization, **data) -> Vendor:
        validate_vendor_ownership(vendor=vendor, organization=organization)
        for field, value in data.items():
            setattr(vendor, field, value)
        vendor.save(update_fields=list(data.keys()) + ['updated_at'])
        return vendor

    @staticmethod
    def assign_owner(*, vendor: Vendor, organization: Organization, owner_user) -> Vendor:
        validate_vendor_ownership(vendor=vendor, organization=organization)
        vendor.owner_user = owner_user
        vendor.save(update_fields=['owner_user', 'updated_at'])
        return vendor

    @staticmethod
    def change_operational_status(*, vendor: Vendor, organization: Organization, status: str) -> Vendor:
        validate_vendor_ownership(vendor=vendor, organization=organization)
        vendor.operational_status = status
        vendor.save(update_fields=['operational_status', 'updated_at'])
        return vendor