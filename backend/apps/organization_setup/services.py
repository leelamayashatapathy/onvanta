from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.approvals.models import ApprovalFlow, ApprovalStep
from apps.document_types.models import DocumentType
from apps.document_types.services import DocumentTypeService
from apps.document_types.validators import validate_document_type_ownership
from apps.onboarding.services import OnboardingTemplateService
from apps.organizations.models import Organization, OrganizationSetupProgress
from apps.organizations.services import OrganizationInviteService


class OrganizationSetupService:
    @staticmethod
    def update_profile(*, organization: Organization, **data) -> Organization:
        allowed = {'name', 'industry', 'size', 'timezone', 'settings_json'}
        updates = {k: v for k, v in data.items() if k in allowed}
        for field, value in updates.items():
            setattr(organization, field, value)
        if updates:
            organization.save(update_fields=list(updates.keys()) + ['updated_at'])
        progress, _ = OrganizationSetupProgress.objects.get_or_create(organization=organization)
        progress.profile_completed = True
        progress.save(update_fields=['profile_completed', 'updated_at'])
        return organization

    @staticmethod
    def invite_members(*, organization: Organization, invites: list[dict], invited_by) -> list[dict]:
        created = []
        for item in invites:
            email = item.get('email', '').lower()
            role = item.get('role')
            if not email or not role:
                raise ValidationError('Invite email and role are required.')
            invite = OrganizationInviteService.create_invite(
                organization=organization,
                email=email,
                role=role,
                invited_by=invited_by,
            )
            created.append({'email': invite.email, 'role': invite.role, 'token': invite.token})
        progress, _ = OrganizationSetupProgress.objects.get_or_create(organization=organization)
        progress.members_invited = True
        progress.save(update_fields=['members_invited', 'updated_at'])
        return created

    @staticmethod
    def save_vendor_categories(*, organization: Organization, categories: list[str]) -> None:
        settings = organization.settings_json or {}
        settings['vendor_categories'] = categories
        organization.settings_json = settings
        organization.save(update_fields=['settings_json', 'updated_at'])
        progress, _ = OrganizationSetupProgress.objects.get_or_create(organization=organization)
        progress.vendor_categories_configured = True
        progress.save(update_fields=['vendor_categories_configured', 'updated_at'])

    @staticmethod
    @transaction.atomic
    def save_document_types(*, organization: Organization, document_types: list[dict]) -> list[DocumentType]:
        created = []
        for payload in document_types:
            created.append(DocumentTypeService.create_document_type(organization=organization, **payload))
        progress, _ = OrganizationSetupProgress.objects.get_or_create(organization=organization)
        progress.document_types_configured = True
        progress.save(update_fields=['document_types_configured', 'updated_at'])
        return created

    @staticmethod
    @transaction.atomic
    def save_templates(*, organization: Organization, templates: list[dict]) -> None:
        for template_payload in templates:
            requirements = template_payload.pop('requirements', [])
            template = OnboardingTemplateService.create_template(organization=organization, **template_payload)
            for req in requirements:
                document_type_id = req.get('document_type_id')
                document_type = DocumentType.objects.get(id=document_type_id)
                validate_document_type_ownership(document_type=document_type, organization=organization)
                OnboardingTemplateService.add_requirement(
                    template=template,
                    document_type=document_type,
                    required=req.get('required', True),
                    sequence=req.get('sequence', 0),
                    review_required=req.get('review_required', True),
                )
        progress, _ = OrganizationSetupProgress.objects.get_or_create(organization=organization)
        progress.onboarding_templates_configured = True
        progress.save(update_fields=['onboarding_templates_configured', 'updated_at'])

    @staticmethod
    @transaction.atomic
    def save_approval_flow(*, organization: Organization, flow: dict) -> ApprovalFlow:
        name = flow.get('name')
        scope = flow.get('scope', 'onboarding')
        steps = flow.get('steps', [])
        approval_flow = ApprovalFlow.objects.create(
            organization=organization,
            name=name,
            scope=scope,
            active=True,
        )
        for step in steps:
            explicit_user_id = step.get('explicit_user_id')
            explicit_user = None
            if explicit_user_id:
                explicit_user = get_user_model().objects.get(id=explicit_user_id)
            ApprovalStep.objects.create(
                flow=approval_flow,
                step_order=step.get('step_order', 0),
                role_required=step.get('role_required', ''),
                explicit_user=explicit_user,
                decision_type=step.get('decision_type', 'single'),
                active=step.get('active', True),
            )
        progress, _ = OrganizationSetupProgress.objects.get_or_create(organization=organization)
        progress.approval_flow_configured = True
        progress.save(update_fields=['approval_flow_configured', 'updated_at'])
        return approval_flow

    @staticmethod
    def save_notification_settings(*, organization: Organization, settings_payload: dict) -> None:
        settings = organization.settings_json or {}
        settings['notification_settings'] = settings_payload
        organization.settings_json = settings
        organization.save(update_fields=['settings_json', 'updated_at'])
        progress, _ = OrganizationSetupProgress.objects.get_or_create(organization=organization)
        progress.notifications_configured = True
        progress.save(update_fields=['notifications_configured', 'updated_at'])

    @staticmethod
    def complete_setup(*, organization: Organization) -> OrganizationSetupProgress:
        progress, _ = OrganizationSetupProgress.objects.get_or_create(organization=organization)
        required = [
            progress.profile_completed,
            progress.vendor_categories_configured,
            progress.document_types_configured,
            progress.onboarding_templates_configured,
            progress.approval_flow_configured,
            progress.notifications_configured,
        ]
        if not all(required):
            raise ValidationError('Setup is incomplete.')
        progress.setup_completed = True
        progress.save(update_fields=['setup_completed', 'updated_at'])
        return progress
