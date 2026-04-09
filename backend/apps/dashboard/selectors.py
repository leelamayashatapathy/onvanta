from __future__ import annotations

from django.db.models import Count
from django.utils import timezone

from apps.approvals.models import ApprovalDecision
from apps.onboarding.enums import OnboardingCaseStatus
from apps.onboarding.models import OnboardingCase
from apps.organizations.models import Organization
from apps.vendor_documents.enums import DocumentStatus
from apps.vendor_documents.models import VendorDocument
from apps.vendors.models import Vendor


def get_org_summary(*, organization: Organization) -> dict:
    return {
        'vendors_total': Vendor.objects.filter(organization=organization).count(),
        'vendors_active': Vendor.objects.filter(
            organization=organization, operational_status='active'
        ).count(),
        'onboarding_active': OnboardingCase.objects.filter(
            organization=organization,
            status__in=[
                OnboardingCaseStatus.COLLECTING_DOCUMENTS,
                OnboardingCaseStatus.UNDER_REVIEW,
                OnboardingCaseStatus.APPROVAL_PENDING,
            ],
        ).count(),
    }


def get_pending_approval_counts(*, organization: Organization) -> dict:
    return {
        'pending_approvals': ApprovalDecision.objects.filter(
            organization=organization, decision='pending'
        ).count()
    }


def get_pipeline_stats(*, organization: Organization) -> dict:
    rows = (
        OnboardingCase.objects.filter(organization=organization)
        .values('status')
        .annotate(total=Count('id'))
    )
    return {row['status']: row['total'] for row in rows}


def get_expiry_stats(*, organization: Organization) -> dict:
    today = timezone.now().date()
    upcoming = VendorDocument.objects.filter(
        organization=organization,
        expiry_date__isnull=False,
        expiry_date__gte=today,
        status=DocumentStatus.ACTIVE,
    ).count()
    overdue = VendorDocument.objects.filter(
        organization=organization,
        expiry_date__isnull=False,
        expiry_date__lt=today,
        status=DocumentStatus.ACTIVE,
    ).count()
    return {'upcoming': upcoming, 'overdue': overdue}