from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.organizations.enums import OrganizationMemberRole, OrganizationMemberStatus
from apps.organizations.models import Organization, OrganizationMember
from apps.vendors.models import Vendor


class VendorStep4Tests(TestCase):
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

    def test_vendor_status_summary(self):
        vendor = Vendor.objects.create(
            organization=self.org,
            vendor_code='V001',
            legal_name='Acme Vendor',
            display_name='Acme Vendor',
        )
        response = self.client.get(f'/api/v1/vendors/{vendor.id}/status-summary/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_documents', response.data['data'])
