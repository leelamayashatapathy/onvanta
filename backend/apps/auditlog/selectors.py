from __future__ import annotations

from django.db import models
from django.db.models import QuerySet

from apps.organizations.models import Organization

from .models import AuditEvent


def list_audit_events(*, organization: Organization) -> QuerySet[AuditEvent]:
    return AuditEvent.objects.filter(organization=organization).order_by('-created_at')


def list_vendor_audit_events(*, organization: Organization, vendor_id) -> QuerySet[AuditEvent]:
    return AuditEvent.objects.filter(
        organization=organization,
        entity_type='Vendor',
        entity_id=vendor_id,
    ).order_by('-created_at')


def list_vendor_related_events(*, organization: Organization, vendor_id) -> QuerySet[AuditEvent]:
    return AuditEvent.objects.filter(
        organization=organization,
    ).filter(
        models.Q(entity_type='Vendor', entity_id=vendor_id)
        | models.Q(new_data_json__vendor_id=str(vendor_id))
    ).order_by('-created_at')
