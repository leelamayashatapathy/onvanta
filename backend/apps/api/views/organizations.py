from __future__ import annotations

from django.utils.text import slugify
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.permissions import CanManageOrgSettings, IsOrganizationMember
from apps.api.responses import success_response
from apps.organizations.enums import OrganizationMemberRole, OrganizationMemberStatus
from apps.organizations.models import Organization, OrganizationMember


class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response(
                {'message': 'Organization name required.', 'error_code': 'missing_name'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        organization = Organization.objects.create(
            name=name,
            slug=slugify(name),
            industry=request.data.get('industry', ''),
            size=request.data.get('size', ''),
            timezone=request.data.get('timezone', 'UTC'),
            settings_json=request.data.get('settings_json', {}),
        )
        OrganizationMember.objects.create(
            organization=organization,
            user=request.user,
            role=OrganizationMemberRole.ORG_ADMIN,
            status=OrganizationMemberStatus.ACTIVE,
        )
        return Response(
            success_response('Organization created.', {'id': str(organization.id), 'name': organization.name}),
            status=status.HTTP_201_CREATED,
        )


class OrganizationDetailView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request):
        org = request.organization
        data = {
            'id': str(org.id),
            'name': org.name,
            'slug': org.slug,
            'industry': org.industry,
            'size': org.size,
            'timezone': org.timezone,
            'settings_json': org.settings_json,
        }
        return Response(success_response('Organization detail.', data), status=200)


class OrganizationMembersView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request):
        members = request.organization.members.select_related('user').order_by('created_at')
        data = [
            {
                'id': str(m.id),
                'user_id': str(m.user_id),
                'email': m.user.email,
                'role': m.role,
                'status': m.status,
            }
            for m in members
        ]
        return Response(success_response('Organization members.', data), status=200)


class OrganizationMemberRoleUpdateView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOrgSettings]

    def post(self, request, member_id):
        role = request.data.get('role')
        if not role:
            return Response(
                {'message': 'Role required.', 'error_code': 'missing_role'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        member = request.organization.members.select_related('user').get(id=member_id)
        member.role = role
        member.save(update_fields=['role', 'updated_at'])
        return Response(success_response('Member role updated.', {'id': str(member.id), 'role': member.role}))
