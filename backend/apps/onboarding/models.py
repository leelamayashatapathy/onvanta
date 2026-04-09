from __future__ import annotations

from django.db import models

from apps.common.models import TimeStampedUUIDModel
from apps.document_types.models import DocumentType
from apps.organizations.models import Organization
from apps.vendors.models import Vendor

from .enums import OnboardingCaseStatus, OnboardingRequirementStatus


class OnboardingTemplate(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='onboarding_templates'
    )
    name = models.CharField(max_length=255)
    applies_to_vendor_category = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'active']),
            models.Index(fields=['organization', 'created_at']),
        ]

    def __str__(self) -> str:
        return self.name


class OnboardingTemplateRequirement(TimeStampedUUIDModel):
    template = models.ForeignKey(
        OnboardingTemplate, on_delete=models.CASCADE, related_name='requirements'
    )
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, related_name='template_requirements'
    )
    required = models.BooleanField(default=True)
    sequence = models.PositiveIntegerField(default=0)
    review_required = models.BooleanField(default=True)

    class Meta:
        unique_together = (('template', 'document_type'),)
        indexes = [
            models.Index(fields=['template', 'sequence']),
        ]

    def __str__(self) -> str:
        return f'{self.template.name} - {self.document_type.name}'


class OnboardingCase(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='onboarding_cases'
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='onboarding_cases')
    template = models.ForeignKey(
        OnboardingTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='cases'
    )
    current_stage = models.CharField(max_length=50, blank=True)
    status = models.CharField(
        max_length=30, choices=OnboardingCaseStatus.choices, default=OnboardingCaseStatus.NOT_STARTED
    )
    progress_percent = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    blocked_reason = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['organization', 'vendor']),
        ]

    def __str__(self) -> str:
        return f'{self.vendor.display_name} onboarding'


class OnboardingRequirement(TimeStampedUUIDModel):
    case = models.ForeignKey(OnboardingCase, on_delete=models.CASCADE, related_name='requirements')
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    required = models.BooleanField(default=True)
    submitted = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    current_document = models.ForeignKey(
        'vendor_documents.VendorDocument',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='onboarding_requirements',
    )
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=OnboardingRequirementStatus.choices, default=OnboardingRequirementStatus.PENDING
    )

    class Meta:
        unique_together = (('case', 'document_type'),)
        indexes = [
            models.Index(fields=['case', 'status']),
            models.Index(fields=['case', 'required']),
        ]

    def __str__(self) -> str:
        return f'{self.case.id} - {self.document_type.name}'