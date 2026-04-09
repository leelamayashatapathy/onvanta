from __future__ import annotations

from django.utils import timezone

from apps.organizations.models import Organization

from .models import NotificationLog


class NotificationService:
    @staticmethod
    def send_reminder(*, organization: Organization, reminder) -> None:
        NotificationLog.objects.create(
            organization=organization,
            channel='email',
            recipient='noreply@example.com',
            template_code='expiry_reminder',
            payload_json={
                'vendor_id': str(reminder.vendor_document.vendor_id),
                'document_id': str(reminder.vendor_document.id),
                'expiry_date': str(reminder.vendor_document.expiry_date),
            },
            sent_at=timezone.now(),
            status='sent',
        )