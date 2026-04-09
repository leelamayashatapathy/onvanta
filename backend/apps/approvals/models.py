from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedUUIDModel
from apps.organizations.models import Organization

from .enums import ApprovalDecisionStatus


class ApprovalFlow(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='approval_flows'
    )
    name = models.CharField(max_length=255)
    scope = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'active']),
            models.Index(fields=['organization', 'scope']),
        ]

    def __str__(self) -> str:
        return self.name


class ApprovalStep(TimeStampedUUIDModel):
    flow = models.ForeignKey(ApprovalFlow, on_delete=models.CASCADE, related_name='steps')
    step_order = models.PositiveIntegerField()
    role_required = models.CharField(max_length=50)
    explicit_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approval_steps',
    )
    decision_type = models.CharField(max_length=20, default='single')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('flow', 'step_order'),)
        indexes = [
            models.Index(fields=['flow', 'step_order']),
        ]

    def __str__(self) -> str:
        return f'{self.flow.name} - {self.step_order}'


class ApprovalDecision(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='approval_decisions'
    )
    onboarding_case = models.ForeignKey(
        'onboarding.OnboardingCase', on_delete=models.CASCADE, related_name='approval_decisions'
    )
    approval_step = models.ForeignKey(
        ApprovalStep, on_delete=models.CASCADE, related_name='decisions'
    )
    decision = models.CharField(
        max_length=20, choices=ApprovalDecisionStatus.choices, default=ApprovalDecisionStatus.PENDING
    )
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approval_decisions',
    )
    decided_at = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'decision']),
            models.Index(fields=['organization', 'created_at']),
        ]

    def __str__(self) -> str:
        return f'{self.onboarding_case_id} - {self.approval_step_id}'