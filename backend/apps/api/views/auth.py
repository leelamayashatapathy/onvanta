from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.responses import success_response
from apps.organizations.models import OrganizationMember


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'message': 'Email and password required.', 'error_code': 'missing_credentials'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_user_model().objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return Response(
                {'message': 'Invalid credentials.', 'error_code': 'invalid_credentials'},
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
                {'message': 'Refresh token required.', 'error_code': 'missing_refresh'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(refresh_token)
        except Exception:
            return Response(
                {'message': 'Invalid refresh token.', 'error_code': 'invalid_refresh'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {'access': str(refresh.access_token)}
        return Response(success_response('Token refreshed.', data), status=200)


class CurrentUserView(APIView):
    def get(self, request):
        memberships = OrganizationMember.objects.filter(user=request.user).select_related('organization')
        data = {
            'id': str(request.user.id),
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'memberships': [
                {
                    'organization_id': str(m.organization_id),
                    'organization_name': m.organization.name,
                    'role': m.role,
                    'status': m.status,
                }
                for m in memberships
            ],
        }
        return Response(success_response('Current user.', data), status=200)
