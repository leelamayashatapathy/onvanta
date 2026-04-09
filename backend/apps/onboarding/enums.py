from django.db import models


class OnboardingCaseStatus(models.TextChoices):
    NOT_STARTED = 'not_started', 'Not Started'
    COLLECTING_DOCUMENTS = 'collecting_documents', 'Collecting Documents'
    UNDER_REVIEW = 'under_review', 'Under Review'
    APPROVAL_PENDING = 'approval_pending', 'Approval Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    CANCELLED = 'cancelled', 'Cancelled'
    COMPLETED = 'completed', 'Completed'


class OnboardingRequirementStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SUBMITTED = 'submitted', 'Submitted'
    VERIFIED = 'verified', 'Verified'
    REJECTED = 'rejected', 'Rejected'