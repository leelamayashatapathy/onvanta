from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedUUIDModel
from apps.organizations.models import Organization

from .enums import VendorOnboardingStatus, VendorOperationalStatus, VendorRiskLevel


class Vendor(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='vendors'
    )
    vendor_code = models.CharField(max_length=50)
    legal_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    vendor_type = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    risk_level = models.CharField(
        max_length=20, choices=VendorRiskLevel.choices, default=VendorRiskLevel.LOW
    )
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    onboarding_status = models.CharField(
        max_length=30, choices=VendorOnboardingStatus.choices, default=VendorOnboardingStatus.DRAFT
    )
    operational_status = models.CharField(
        max_length=20, choices=VendorOperationalStatus.choices, default=VendorOperationalStatus.INACTIVE
    )
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = (('organization', 'vendor_code'),)
        indexes = [
            models.Index(fields=['organization', 'onboarding_status']),
            models.Index(fields=['organization', 'operational_status']),
            models.Index(fields=['organization', 'created_at']),
        ]

    def __str__(self) -> str:
        return f'{self.display_name} ({self.vendor_code})'


class VendorContact(TimeStampedUUIDModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['vendor', 'is_primary']),
        ]

    def __str__(self) -> str:
        return f'{self.name} ({self.vendor.display_name})'