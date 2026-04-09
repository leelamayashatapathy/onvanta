from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.organizations.models import Organization
from apps.vendors.models import Vendor

from .models import OnboardingCase, OnboardingTemplate


def validate_vendor_ownership(*, vendor: Vendor, organization: Organization) -> None:
    if vendor.organization_id != organization.id:
        raise ValidationError('Vendor does not belong to this organization.')


def validate_template_ownership(*, template: OnboardingTemplate, organization: Organization) -> None:
    if template.organization_id != organization.id:
        raise ValidationError('Template does not belong to this organization.')


def ensure_no_active_case(*, vendor: Vendor) -> None:
    if OnboardingCase.objects.filter(vendor=vendor).exclude(status__in=['cancelled', 'completed']).exists():
        raise ValidationError('An active onboarding case already exists for this vendor.')
