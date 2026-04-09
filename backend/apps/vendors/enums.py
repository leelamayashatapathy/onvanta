from django.db import models


class VendorOnboardingStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    DOCUMENTS_PENDING = 'documents_pending', 'Documents Pending'
    UNDER_REVIEW = 'under_review', 'Under Review'
    APPROVAL_PENDING = 'approval_pending', 'Approval Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    ACTIVE = 'active', 'Active'
    RESTRICTED = 'restricted', 'Restricted'
    ARCHIVED = 'archived', 'Archived'


class VendorOperationalStatus(models.TextChoices):
    INACTIVE = 'inactive', 'Inactive'
    ACTIVE = 'active', 'Active'
    RESTRICTED = 'restricted', 'Restricted'
    SUSPENDED = 'suspended', 'Suspended'


class VendorRiskLevel(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'
    CRITICAL = 'critical', 'Critical'