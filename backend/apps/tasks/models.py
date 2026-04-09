from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedUUIDModel
from apps.organizations.models import Organization

from .enums import TaskPriority, TaskStatus


class ActionTask(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='tasks'
    )
    vendor = models.ForeignKey(
        'vendors.Vendor', null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks'
    )
    onboarding_case = models.ForeignKey(
        'onboarding.OnboardingCase',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks',
    )
    task_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_tasks',
    )
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.OPEN)
    priority = models.CharField(
        max_length=20, choices=TaskPriority.choices, default=TaskPriority.MEDIUM
    )

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['organization', 'due_date']),
        ]

    def __str__(self) -> str:
        return self.title