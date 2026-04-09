from __future__ import annotations

from django.utils import timezone

from apps.auditlog.services import AuditService
from apps.onboarding.enums import OnboardingCaseStatus
from apps.organizations.models import Organization
from apps.vendors.enums import VendorOnboardingStatus, VendorOperationalStatus

from .enums import ApprovalDecisionStatus
from .models import ApprovalDecision, ApprovalFlow, ApprovalStep
from .validators import (
    validate_case_ownership,
    validate_decision_actor,
    validate_decision_pending,
    validate_flow_ownership,
)


class ApprovalService:
    @staticmethod
    def submit_case(*, organization: Organization, onboarding_case, flow: ApprovalFlow, actor) -> None:
        validate_case_ownership(onboarding_case=onboarding_case, organization=organization)
        validate_flow_ownership(flow=flow, organization=organization)

        steps = flow.steps.filter(active=True).order_by('step_order')
        decisions = [
            ApprovalDecision(
                organization=organization,
                onboarding_case=onboarding_case,
                approval_step=step,
                decision=ApprovalDecisionStatus.PENDING,
            )
            for step in steps
        ]
        ApprovalDecision.objects.bulk_create(decisions)

        onboarding_case.status = OnboardingCaseStatus.APPROVAL_PENDING
        onboarding_case.current_stage = 'approval'
        onboarding_case.save(update_fields=['status', 'current_stage', 'updated_at'])

        onboarding_case.vendor.onboarding_status = VendorOnboardingStatus.APPROVAL_PENDING
        onboarding_case.vendor.save(update_fields=['onboarding_status', 'updated_at'])

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='OnboardingCase',
            entity_id=onboarding_case.id,
            action='approval_submitted',
            source='api',
            new_data={'case_id': str(onboarding_case.id), 'flow_id': str(flow.id)},
        )

    @staticmethod
    def approve_step(
        *, decision: ApprovalDecision, organization: Organization, actor, actor_role: str, comments: str = ''
    ) -> ApprovalDecision:
        validate_case_ownership(onboarding_case=decision.onboarding_case, organization=organization)
        validate_decision_pending(decision=decision)
        validate_decision_actor(decision=decision, actor=actor, actor_role=actor_role)

        decision.decision = ApprovalDecisionStatus.APPROVED
        decision.decided_by = actor
        decision.decided_at = timezone.now()
        decision.comments = comments or ''
        decision.save(update_fields=['decision', 'decided_by', 'decided_at', 'comments', 'updated_at'])

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='ApprovalDecision',
            entity_id=decision.id,
            action='approval_step_approved',
            source='api',
            new_data={'decision_id': str(decision.id), 'case_id': str(decision.onboarding_case_id)},
        )

        ApprovalService._finalize_if_complete(
            onboarding_case=decision.onboarding_case, organization=organization, actor=actor
        )
        return decision

    @staticmethod
    def reject_step(
        *, decision: ApprovalDecision, organization: Organization, actor, actor_role: str, comments: str
    ) -> ApprovalDecision:
        validate_case_ownership(onboarding_case=decision.onboarding_case, organization=organization)
        validate_decision_pending(decision=decision)
        validate_decision_actor(decision=decision, actor=actor, actor_role=actor_role)

        decision.decision = ApprovalDecisionStatus.REJECTED
        decision.decided_by = actor
        decision.decided_at = timezone.now()
        decision.comments = comments or ''
        decision.save(update_fields=['decision', 'decided_by', 'decided_at', 'comments', 'updated_at'])

        decision.onboarding_case.status = OnboardingCaseStatus.REJECTED
        decision.onboarding_case.save(update_fields=['status', 'updated_at'])

        decision.onboarding_case.vendor.onboarding_status = VendorOnboardingStatus.REJECTED
        decision.onboarding_case.vendor.save(update_fields=['onboarding_status', 'updated_at'])

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='ApprovalDecision',
            entity_id=decision.id,
            action='approval_step_rejected',
            source='api',
            new_data={'decision_id': str(decision.id), 'case_id': str(decision.onboarding_case_id)},
        )

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='OnboardingCase',
            entity_id=decision.onboarding_case.id,
            action='approval_rejected',
            source='api',
            new_data={'case_id': str(decision.onboarding_case.id)},
        )
        return decision

    @staticmethod
    def _finalize_if_complete(*, onboarding_case, organization: Organization, actor) -> None:
        if onboarding_case.approval_decisions.filter(decision=ApprovalDecisionStatus.PENDING).exists():
            return

        onboarding_case.status = OnboardingCaseStatus.APPROVED
        onboarding_case.completed_at = timezone.now()
        onboarding_case.save(update_fields=['status', 'completed_at', 'updated_at'])

        onboarding_case.vendor.onboarding_status = VendorOnboardingStatus.ACTIVE
        onboarding_case.vendor.operational_status = VendorOperationalStatus.ACTIVE
        onboarding_case.vendor.save(update_fields=['onboarding_status', 'operational_status', 'updated_at'])

        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='OnboardingCase',
            entity_id=onboarding_case.id,
            action='approval_completed',
            source='api',
            new_data={'case_id': str(onboarding_case.id)},
        )