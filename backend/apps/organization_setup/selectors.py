from __future__ import annotations

from apps.organizations.models import Organization, OrganizationSetupProgress


def get_setup_status(*, organization: Organization) -> OrganizationSetupProgress:
    progress, _ = OrganizationSetupProgress.objects.get_or_create(organization=organization)
    return progress
