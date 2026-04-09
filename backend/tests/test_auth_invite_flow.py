from __future__ import annotations

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.organizations.enums import OrganizationInviteStatus, OrganizationMemberRole, OrganizationMemberStatus
from apps.organizations.models import Organization, OrganizationInvite, OrganizationMember
from apps.organizations.services import OrganizationInviteService


class InviteFlowTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.organization = Organization.objects.create(
            name='Acme Corp',
            slug='acme-corp',
            industry='Manufacturing',
            size='100-500',
            timezone='UTC',
        )

    def test_accept_invite_valid(self):
        invite = OrganizationInviteService.create_invite(
            organization=self.organization,
            email='owner@acme.test',
            role=OrganizationMemberRole.ORG_ADMIN,
        )
        response = self.client.post('/api/v1/auth/accept-invite/', {'token': invite.token}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['organization_id'], str(self.organization.id))
        self.assertEqual(response.data['data']['email'], 'owner@acme.test')

    def test_accept_invite_expired(self):
        invite = OrganizationInvite.objects.create(
            organization=self.organization,
            email='expired@acme.test',
            role=OrganizationMemberRole.REVIEWER,
            token='expiredtoken',
            expires_at=timezone.now() - timedelta(hours=1),
            status=OrganizationInviteStatus.PENDING,
        )
        response = self.client.post('/api/v1/auth/accept-invite/', {'token': invite.token}, format='json')
        invite.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(invite.status, OrganizationInviteStatus.EXPIRED)

    def test_set_password_from_invite_creates_user_and_membership(self):
        invite = OrganizationInviteService.create_invite(
            organization=self.organization,
            email='member@acme.test',
            role=OrganizationMemberRole.REVIEWER,
        )
        response = self.client.post(
            '/api/v1/auth/set-password-from-invite/',
            {'token': invite.token, 'password': 'StrongPass123!', 'first_name': 'Jane', 'last_name': 'Doe'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get(email='member@acme.test')
        member = OrganizationMember.objects.get(organization=self.organization, user=user)
        invite.refresh_from_db()
        self.assertTrue(user.check_password('StrongPass123!'))
        self.assertEqual(member.status, OrganizationMemberStatus.ACTIVE)
        self.assertEqual(invite.status, OrganizationInviteStatus.ACCEPTED)


class CurrentUserViewTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_me_includes_platform_admin_flag(self):
        user = get_user_model().objects.create_user(
            email='admin@platform.test',
            password='Pass1234!',
            is_platform_admin=True,
        )
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['data']['is_platform_admin'])
