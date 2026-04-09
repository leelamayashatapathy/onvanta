from __future__ import annotations

from celery import shared_task

from apps.organizations.models import Organization

from .services import ExpiryService


@shared_task
def nightly_expiry_scan():
    for org in Organization.objects.all():
        ExpiryService.mark_expired_documents(organization=org)
        ExpiryService.restrict_vendor_if_required(organization=org)
        ExpiryService.create_reminder_schedules(organization=org)


@shared_task
def execute_scheduled_reminders():
    for org in Organization.objects.all():
        ExpiryService.execute_reminders(organization=org)