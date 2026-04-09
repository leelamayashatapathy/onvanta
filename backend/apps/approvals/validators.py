from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.organizations.models import Organization

from .models import ApprovalDecision, ApprovalFlow


def validate_flow_ownership(*, flow: ApprovalFlow, organization: Organization) -> None:
    if flow.organization_id != organization.id:
        raise ValidationError('Approval flow does not belong to this organization.')


def validate_case_ownership(*, onboarding_case, organization: Organization) -> None:
    if onboarding_case.organization_id != organization.id:
        raise ValidationError('Onboarding case does not belong to this organization.')


def validate_decision_pending(*, decision: ApprovalDecision) -> None:
    if decision.decision != 'pending':
        raise ValidationError('Decision is already finalized.')


def validate_decision_actor(*, decision: ApprovalDecision, actor, actor_role: str) -> None:
    step = decision.approval_step
    if step.explicit_user_id and step.explicit_user_id != actor.id:
        raise ValidationError('Only the assigned approver can take this decision.')
    if step.role_required and actor_role != step.role_required:
        raise ValidationError('Your role is not allowed to take this decision.')