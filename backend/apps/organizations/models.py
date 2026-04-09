from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedUUIDModel

from .enums import OrganizationMemberRole, OrganizationMemberStatus


class Organization(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    industry = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=64, default='UTC')
    settings_json = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return self.name


class OrganizationMember(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='members'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organization_memberships'
    )
    role = models.CharField(max_length=50, choices=OrganizationMemberRole.choices)
    status = models.CharField(
        max_length=20, choices=OrganizationMemberStatus.choices, default=OrganizationMemberStatus.INVITED
    )

    class Meta:
        unique_together = (('organization', 'user'),)
        indexes = [
            models.Index(fields=['organization', 'role']),
            models.Index(fields=['organization', 'status']),
        ]

    def __str__(self) -> str:
        return f'{self.organization} - {self.user.email}'