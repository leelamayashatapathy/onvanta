from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.permissions import IsPlatformAdmin
from apps.api.responses import error_response, success_response
from apps.organizations.models import Organization
from apps.organizations.services import OrganizationRegistrationService
from apps.platform_admin.selectors import get_organization_detail, list_organizations
from apps.platform_admin.services import PlatformAdminOrganizationService


class PlatformAdminDashboardView(APIView):
    permission_classes = [IsPlatformAdmin]

    def get(self, request):
        data = {
            'organizations_count': Organization.objects.count(),
            'users_count': get_user_model().objects.count(),
        }
        return Response(success_response('Platform dashboard.', data), status=200)


class PlatformAdminOrganizationListView(APIView):
    permission_classes = [IsPlatformAdmin]

    def get(self, request):
        orgs = list_organizations()
        data = [
            {
                'id': str(o.id),
                'name': o.name,
                'slug': o.slug,
                'industry': o.industry,
                'size': o.size,
                'timezone': o.timezone,
                'status': o.status,
                'created_at': o.created_at,
            }
            for o in orgs
        ]
        return Response(success_response('Organizations.', data), status=200)


class PlatformAdminOrganizationDetailView(APIView):
    permission_classes = [IsPlatformAdmin]

    def get(self, request, org_id):
        org = get_organization_detail(organization_id=org_id)
        data = {
            'id': str(org.id),
            'name': org.name,
            'slug': org.slug,
            'industry': org.industry,
            'size': org.size,
            'timezone': org.timezone,
            'status': org.status,
            'settings_json': org.settings_json,
            'created_at': org.created_at,
        }
        return Response(success_response('Organization detail.', data), status=200)


class PlatformAdminOrganizationCreateView(APIView):
    permission_classes = [IsPlatformAdmin]

    @transaction.atomic
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response(error_response('Name required.', 'missing_name'), status=status.HTTP_400_BAD_REQUEST)
        org = OrganizationRegistrationService.create_organization(
            name=name,
            industry=request.data.get('industry', ''),
            size=request.data.get('size', ''),
            timezone=request.data.get('timezone', 'UTC'),
        )
        return Response(
            success_response('Organization created.', {'id': str(org.id), 'name': org.name}),
            status=status.HTTP_201_CREATED,
        )


class PlatformAdminInviteOrgAdminView(APIView):
    permission_classes = [IsPlatformAdmin]

    def post(self, request, org_id):
        email = request.data.get('email')
        if not email:
            return Response(error_response('Email required.', 'missing_email'), status=status.HTTP_400_BAD_REQUEST)
        org = get_organization_detail(organization_id=org_id)
        data = PlatformAdminOrganizationService.invite_admin(
            organization=org,
            email=email,
            invited_by=request.user,
        )
        return Response(success_response('Invite created.', data), status=status.HTTP_201_CREATED)


class PlatformAdminOrganizationStatusUpdateView(APIView):
    permission_classes = [IsPlatformAdmin]

    def patch(self, request, org_id):
        status_value = request.data.get('status')
        if not status_value:
            return Response(error_response('Status required.', 'missing_status'), status=status.HTTP_400_BAD_REQUEST)
        org = get_organization_detail(organization_id=org_id)
        org = PlatformAdminOrganizationService.update_organization_status(organization=org, status=status_value)
        return Response(success_response('Organization status updated.', {'id': str(org.id), 'status': org.status}))
