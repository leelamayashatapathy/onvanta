from __future__ import annotations

from django.db.models import QuerySet

from apps.organizations.models import Organization


def list_organizations() -> QuerySet[Organization]:
    return Organization.objects.all().order_by('-created_at')


def get_organization_detail(*, organization_id) -> Organization:
    return Organization.objects.get(id=organization_id)
