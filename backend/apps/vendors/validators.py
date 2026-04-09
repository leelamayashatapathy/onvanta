from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.organizations.models import Organization

from .models import Vendor


def validate_vendor_ownership(*, vendor: Vendor, organization: Organization) -> None:
    if vendor.organization_id != organization.id:
        raise ValidationError('Vendor does not belong to this organization.')