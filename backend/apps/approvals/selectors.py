from __future__ import annotations

from django.db.models import QuerySet

from apps.organizations.models import Organization

from .models import ApprovalDecision, ApprovalFlow


def get_active_flow(*, organization: Organization, scope: str) -> ApprovalFlow:
    return ApprovalFlow.objects.get(organization=organization, scope=scope, active=True)


def list_flows(*, organization: Organization) -> QuerySet[ApprovalFlow]:
    return ApprovalFlow.objects.filter(organization=organization).order_by('name')


def get_flow_detail(*, organization: Organization, flow_id) -> ApprovalFlow:
    return ApprovalFlow.objects.prefetch_related('steps').get(id=flow_id, organization=organization)


def list_pending_approvals(*, organization: Organization) -> QuerySet[ApprovalDecision]:
    return (
        ApprovalDecision.objects.filter(organization=organization, decision='pending')
        .select_related('onboarding_case', 'approval_step')
        .order_by('created_at')
    )


def list_case_decisions(*, organization: Organization, case_id) -> QuerySet[ApprovalDecision]:
    return ApprovalDecision.objects.filter(
        organization=organization, onboarding_case_id=case_id
    ).select_related('approval_step', 'decided_by')