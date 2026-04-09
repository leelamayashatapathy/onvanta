from __future__ import annotations

from django.db import models


class ReminderStatus(models.TextChoices):
    SCHEDULED = 'scheduled', 'Scheduled'
    SENT = 'sent', 'Sent'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'


class ReminderType(models.TextChoices):
    EXPIRY_WARNING = 'expiry_warning', 'Expiry Warning'
    EXPIRY_OVERDUE = 'expiry_overdue', 'Expiry Overdue'