from django.db import models

from apps.common.models import TimeStampedUUIDModel
from apps.organizations.models import Organization

from .enums import DocumentCriticality


class DocumentType(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='document_types'
    )
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_mandatory = models.BooleanField(default=False)
    has_expiry = models.BooleanField(default=False)
    expiry_warning_days = models.PositiveIntegerField(default=30)
    criticality = models.CharField(
        max_length=20, choices=DocumentCriticality.choices, default=DocumentCriticality.MEDIUM
    )
    applies_to_vendor_type = models.CharField(max_length=100, blank=True)
    allowed_extensions = models.JSONField(default=list, blank=True)
    max_file_size_mb = models.PositiveIntegerField(default=10)

    class Meta:
        unique_together = (('organization', 'code'),)
        indexes = [
            models.Index(fields=['organization', 'category']),
            models.Index(fields=['organization', 'is_mandatory']),
            models.Index(fields=['organization', 'has_expiry']),
        ]

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'