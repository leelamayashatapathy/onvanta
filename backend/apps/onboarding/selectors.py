from __future__ import annotations

from django.db.models import QuerySet

from apps.organizations.models import Organization

from .enums import OnboardingCaseStatus
from .models import OnboardingCase, OnboardingRequirement, OnboardingTemplate


def list_templates(*, organization: Organization) -> QuerySet[OnboardingTemplate]:
    return OnboardingTemplate.objects.filter(organization=organization).order_by('name')


def get_template_detail(*, organization: Organization, template_id) -> OnboardingTemplate:
    return OnboardingTemplate.objects.prefetch_related('requirements', 'requirements__document_type').get(
        id=template_id, organization=organization
    )


def get_case_detail(*, organization: Organization, case_id) -> OnboardingCase:
    return OnboardingCase.objects.select_related('vendor', 'template').get(
        id=case_id, organization=organization
    )


def list_pending_cases(*, organization: Organization) -> QuerySet[OnboardingCase]:
    return OnboardingCase.objects.filter(
        organization=organization,
        status=OnboardingCaseStatus.UNDER_REVIEW,
    ).select_related('vendor')


def list_blocked_cases(*, organization: Organization) -> QuerySet[OnboardingCase]:
    return OnboardingCase.objects.filter(
        organization=organization,
        blocked_reason__isnull=False,
    ).exclude(blocked_reason='').select_related('vendor')


def get_case_checklist(*, organization: Organization, case_id) -> QuerySet[OnboardingRequirement]:
    return OnboardingRequirement.objects.filter(case_id=case_id, case__organization=organization).select_related(
        'document_type', 'current_document'
    )
