from django.db import models


class OrganizationMemberRole(models.TextChoices):
    ORG_ADMIN = 'org_admin', 'Org Admin'
    PROCUREMENT_MANAGER = 'procurement_manager', 'Procurement Manager'
    REVIEWER = 'reviewer', 'Reviewer'
    APPROVER = 'approver', 'Approver'
    COMPLIANCE_MANAGER = 'compliance_manager', 'Compliance Manager'
    READ_ONLY = 'read_only', 'Read Only'


class OrganizationMemberStatus(models.TextChoices):
    INVITED = 'invited', 'Invited'
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class OrganizationStatus(models.TextChoices):
    TRIAL = 'trial', 'Trial'
    ACTIVE = 'active', 'Active'
    SUSPENDED = 'suspended', 'Suspended'
    ARCHIVED = 'archived', 'Archived'


class OrganizationInviteStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    EXPIRED = 'expired', 'Expired'
    CANCELLED = 'cancelled', 'Cancelled'
