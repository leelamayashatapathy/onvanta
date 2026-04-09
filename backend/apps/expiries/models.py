from __future__ import annotations

from django.db import models

from apps.common.models import TimeStampedUUIDModel
from apps.organizations.models import Organization

from .enums import ReminderStatus, ReminderType


class ReminderSchedule(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='reminder_schedules'
    )
    vendor_document = models.ForeignKey(
        'vendor_documents.VendorDocument',
        on_delete=models.CASCADE,
        related_name='reminders',
    )
    reminder_type = models.CharField(max_length=30, choices=ReminderType.choices)
    scheduled_for = models.DateTimeField()
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ReminderStatus.choices, default=ReminderStatus.SCHEDULED)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['organization', 'scheduled_for']),
        ]

    def __str__(self) -> str:
        return f'{self.vendor_document_id} - {self.reminder_type}'