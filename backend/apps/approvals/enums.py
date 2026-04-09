from django.db import models


class ApprovalDecisionStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    SKIPPED = 'skipped', 'Skipped'