from __future__ import annotations

from django.db.models import QuerySet

from .models import Organization, OrganizationMember


def get_organization(*, organization_id) -> Organization:
    return Organization.objects.get(id=organization_id)


def get_member(*, organization: Organization, user) -> OrganizationMember:
    return OrganizationMember.objects.get(organization=organization, user=user)


def list_members(*, organization: Organization) -> QuerySet[OrganizationMember]:
    return OrganizationMember.objects.filter(organization=organization)