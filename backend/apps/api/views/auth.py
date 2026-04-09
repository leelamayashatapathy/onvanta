from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.responses import error_response, success_response
from apps.organizations.models import OrganizationMember, OrganizationSetupProgress
from apps.organizations.services import OrganizationInviteService


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                error_response('Email and password required.', 'missing_credentials'),
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_user_model().objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return Response(
                error_response('Invalid credentials.', 'invalid_credentials'),
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        return Response(success_response('Login successful.', data), status=200)


class RefreshView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                error_response('Refresh token required.', 'missing_refresh'),
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(refresh_token)
        except Exception:
            return Response(
                error_response('Invalid refresh token.', 'invalid_refresh'),
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {'access': str(refresh.access_token)}
        return Response(success_response('Token refreshed.', data), status=200)


class CurrentUserView(APIView):
    def get(self, request):
        memberships = OrganizationMember.objects.filter(user=request.user).select_related('organization')
        setup_map = {
            str(p.organization_id): p
            for p in OrganizationSetupProgress.objects.filter(
                organization_id__in=[m.organization_id for m in memberships]
            )
        }
        data = {
            'id': str(request.user.id),
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'is_platform_admin': request.user.is_platform_admin,
            'memberships': [
                {
                    'organization_id': str(m.organization_id),
                    'organization_name': m.organization.name,
                    'role': m.role,
                    'status': m.status,
                    'setup_completed': setup_map.get(str(m.organization_id)).setup_completed
                    if setup_map.get(str(m.organization_id))
                    else False,
                }
                for m in memberships
            ],
        }
        return Response(success_response('Current user.', data), status=200)


class AcceptInviteView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        token = request.data.get('token')
        try:
            data = OrganizationInviteService.accept_invite(token=token)
        except ValidationError as exc:
            return Response(
                error_response('Invalid invite token.', 'invalid_invite', exc.detail),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(success_response('Invite valid.', data), status=200)


class SetPasswordFromInviteView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        if not password:
            return Response(
                error_response('Password is required.', 'missing_password'),
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            data = OrganizationInviteService.set_password_from_invite(
                token=token,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
        except ValidationError as exc:
            return Response(
                error_response('Invalid invite token.', 'invalid_invite', exc.detail),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(success_response('Password set.', data), status=200)
