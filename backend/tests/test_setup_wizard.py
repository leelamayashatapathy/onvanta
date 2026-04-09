from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.organizations.enums import OrganizationMemberRole, OrganizationMemberStatus
from apps.organizations.models import Organization, OrganizationMember, OrganizationSetupProgress


class SetupWizardTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.org = Organization.objects.create(name='Acme', slug='acme', timezone='UTC')
        self.user = get_user_model().objects.create_user(email='admin@acme.test', password='Pass1234!')
        OrganizationMember.objects.create(
            organization=self.org,
            user=self.user,
            role=OrganizationMemberRole.ORG_ADMIN,
            status=OrganizationMemberStatus.ACTIVE,
        )
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_X_ORG_ID=str(self.org.id))

    def test_setup_status_default(self):
        response = self.client.get('/api/v1/setup/status/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['data']['setup_completed'])

    def test_setup_profile(self):
        response = self.client.post(
            '/api/v1/setup/organization-profile/',
            {'name': 'Acme Updated', 'industry': 'Finance', 'size': '1-10', 'timezone': 'UTC'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        progress = OrganizationSetupProgress.objects.get(organization=self.org)
        self.assertTrue(progress.profile_completed)
