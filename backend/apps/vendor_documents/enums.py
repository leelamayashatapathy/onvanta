from django.db import models


class DocumentVerificationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    UNDER_REVIEW = 'under_review', 'Under Review'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    EXPIRED = 'expired', 'Expired'
    SUPERSEDED = 'superseded', 'Superseded'


class DocumentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACTIVE = 'active', 'Active'
    REJECTED = 'rejected', 'Rejected'
    EXPIRED = 'expired', 'Expired'
    SUPERSEDED = 'superseded', 'Superseded'