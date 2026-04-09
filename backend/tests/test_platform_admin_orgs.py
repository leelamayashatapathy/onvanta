from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.organizations.models import Organization


class PlatformAdminOrganizationTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.platform_admin = get_user_model().objects.create_user(
            email='platform@onvanta.test',
            password='StrongPass123!',
            is_platform_admin=True,
        )
        self.client.force_authenticate(user=self.platform_admin)

    def test_create_organization(self):
        response = self.client.post(
            '/api/v1/platform-admin/organizations/create/',
            {'name': 'Onvanta Demo', 'industry': 'Tech', 'size': '1-10', 'timezone': 'UTC'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Organization.objects.filter(name='Onvanta Demo').exists())

    def test_invite_org_admin(self):
        org = Organization.objects.create(name='Demo Org', slug='demo-org', timezone='UTC')
        response = self.client.post(
            f'/api/v1/platform-admin/organizations/{org.id}/invite-admin/',
            {'email': 'admin@demo.test'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data['data'])
