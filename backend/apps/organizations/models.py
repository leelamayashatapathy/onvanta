from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedUUIDModel

from .enums import (
    OrganizationInviteStatus,
    OrganizationMemberRole,
    OrganizationMemberStatus,
    OrganizationStatus,
)


class Organization(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    industry = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=64, default='UTC')
    status = models.CharField(
        max_length=20, choices=OrganizationStatus.choices, default=OrganizationStatus.TRIAL
    )
    settings_json = models.JSONField(default=dict, blank=True)
    last_activity_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
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


class OrganizationInvite(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='invites'
    )
    email = models.EmailField()
    role = models.CharField(max_length=50, choices=OrganizationMemberRole.choices)
    token = models.CharField(max_length=64, unique=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_invites'
    )
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=OrganizationInviteStatus.choices, default=OrganizationInviteStatus.PENDING
    )

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['email']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self) -> str:
        return f'{self.email} - {self.organization.name}'


class OrganizationSetupProgress(TimeStampedUUIDModel):
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name='setup_progress'
    )
    profile_completed = models.BooleanField(default=False)
    members_invited = models.BooleanField(default=False)
    vendor_categories_configured = models.BooleanField(default=False)
    document_types_configured = models.BooleanField(default=False)
    onboarding_templates_configured = models.BooleanField(default=False)
    approval_flow_configured = models.BooleanField(default=False)
    notifications_configured = models.BooleanField(default=False)
    setup_completed = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['setup_completed']),
        ]

    def __str__(self) -> str:
        return f'{self.organization.name} setup'
