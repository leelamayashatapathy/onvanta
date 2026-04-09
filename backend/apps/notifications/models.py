from __future__ import annotations

from django.db import models

from apps.common.models import TimeStampedUUIDModel
from apps.organizations.models import Organization


class NotificationLog(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='notification_logs'
    )
    channel = models.CharField(max_length=50)
    recipient = models.CharField(max_length=255)
    template_code = models.CharField(max_length=100)
    payload_json = models.JSONField(default=dict, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['organization', 'sent_at']),
        ]

    def __str__(self) -> str:
        return f'{self.channel} - {self.recipient}'