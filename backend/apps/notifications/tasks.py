from __future__ import annotations

from celery import shared_task

from apps.organizations.models import Organization
from apps.notifications.models import NotificationLog


@shared_task
def weekly_summary_emails():
    # Weekly summary email aggregation (basic stub for MVP).
    for org in Organization.objects.all():
        NotificationLog.objects.create(
            organization=org,
            channel='email',
            recipient='noreply@example.com',
            template_code='weekly_summary',
            payload_json={},
            sent_at=None,
            status='queued',
        )
