from __future__ import annotations

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.permissions import CanManageOrgSettings
from apps.api.responses import error_response, success_response
from apps.organization_setup.selectors import get_setup_status
from apps.organization_setup.services import OrganizationSetupService


class SetupStatusView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def get(self, request):
        progress = get_setup_status(organization=request.organization)
        data = {
            'profile_completed': progress.profile_completed,
            'members_invited': progress.members_invited,
            'vendor_categories_configured': progress.vendor_categories_configured,
            'document_types_configured': progress.document_types_configured,
            'onboarding_templates_configured': progress.onboarding_templates_configured,
            'approval_flow_configured': progress.approval_flow_configured,
            'notifications_configured': progress.notifications_configured,
            'setup_completed': progress.setup_completed,
        }
        return Response(success_response('Setup status.', data), status=200)


class SetupOrganizationProfileView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def post(self, request):
        org = OrganizationSetupService.update_profile(
            organization=request.organization,
            name=request.data.get('name', request.organization.name),
            industry=request.data.get('industry', request.organization.industry),
            size=request.data.get('size', request.organization.size),
            timezone=request.data.get('timezone', request.organization.timezone),
            settings_json=request.data.get('settings_json', request.organization.settings_json),
        )
        data = {'id': str(org.id), 'name': org.name}
        return Response(success_response('Organization profile updated.', data), status=200)


class SetupInviteMembersView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def post(self, request):
        invites = request.data.get('invites', [])
        try:
            created = OrganizationSetupService.invite_members(
                organization=request.organization,
                invites=invites,
                invited_by=request.user,
            )
        except ValidationError as exc:
            return Response(
                error_response('Invalid invites.', 'invalid_invites', {'detail': exc.args[0]}),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(success_response('Invites sent.', created), status=201)


class SetupVendorCategoriesView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def post(self, request):
        categories = request.data.get('categories', [])
        OrganizationSetupService.save_vendor_categories(organization=request.organization, categories=categories)
        return Response(success_response('Vendor categories saved.', {'count': len(categories)}), status=200)


class SetupDocumentTypesView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def post(self, request):
        document_types = request.data.get('document_types', [])
        created = OrganizationSetupService.save_document_types(
            organization=request.organization, document_types=document_types
        )
        data = [{'id': str(dt.id), 'name': dt.name, 'code': dt.code} for dt in created]
        return Response(success_response('Document types saved.', data), status=201)


class SetupOnboardingTemplatesView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def post(self, request):
        templates = request.data.get('templates', [])
        OrganizationSetupService.save_templates(organization=request.organization, templates=templates)
        return Response(success_response('Onboarding templates saved.', {'count': len(templates)}), status=201)


class SetupApprovalFlowView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def post(self, request):
        flow = request.data.get('flow', {})
        approval_flow = OrganizationSetupService.save_approval_flow(
            organization=request.organization, flow=flow
        )
        data = {'id': str(approval_flow.id), 'name': approval_flow.name}
        return Response(success_response('Approval flow saved.', data), status=201)


class SetupNotificationSettingsView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def post(self, request):
        settings_payload = request.data.get('settings', {})
        OrganizationSetupService.save_notification_settings(
            organization=request.organization, settings_payload=settings_payload
        )
        return Response(success_response('Notification settings saved.', {}), status=200)


class SetupCompleteView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def post(self, request):
        try:
            progress = OrganizationSetupService.complete_setup(organization=request.organization)
        except ValidationError:
            return Response(
                error_response('Setup is incomplete.', 'setup_incomplete'),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            success_response('Setup completed.', {'setup_completed': progress.setup_completed}),
            status=200,
        )
