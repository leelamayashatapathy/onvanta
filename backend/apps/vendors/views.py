from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import CanManageVendors, IsOrganizationMember
from apps.api.responses import error_response, success_response
from apps.organizations.models import OrganizationMember
from apps.vendors.models import VendorContact
from apps.vendors.selectors import (
    get_vendor_detail,
    get_vendor_status_summary,
    get_vendor_timeline,
    list_vendors,
)
from apps.vendors.serializers import (
    VendorContactCreateSerializer,
    VendorContactSerializer,
    VendorCreateUpdateSerializer,
    VendorSerializer,
)
from apps.vendors.services import VendorService

User = get_user_model()


def _resolve_owner_user(*, organization, owner_user_id):
    if owner_user_id is None:
        return None
    user = User.objects.filter(id=owner_user_id).first()
    if not user:
        return None
    membership = OrganizationMember.objects.filter(organization=organization, user=user).first()
    if not membership:
        return None
    return user


class VendorListCreateView(OrganizationContextMixin, APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [CanManageVendors()]
        return [IsOrganizationMember()]

    def get(self, request):
        queryset = list_vendors(organization=request.organization)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = VendorSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Vendors retrieved.', serializer.data, metadata), status=200)

    def post(self, request):
        serializer = VendorCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        owner_user_id = data.pop('owner_user', None)
        owner_user = _resolve_owner_user(organization=request.organization, owner_user_id=owner_user_id)
        if owner_user_id and owner_user is None:
            return Response(
                {'message': 'Owner user must be a member of the organization.', 'error_code': 'invalid_owner'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vendor = VendorService.create_vendor(
            organization=request.organization, owner_user=owner_user, actor=request.user, **data
        )
        return Response(
            success_response('Vendor created.', VendorSerializer(vendor).data),
            status=status.HTTP_201_CREATED,
        )


class VendorDetailView(OrganizationContextMixin, APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [CanManageVendors()]
        return [IsOrganizationMember()]

    def get(self, request, vendor_id):
        vendor = get_vendor_detail(organization=request.organization, vendor_id=vendor_id)
        return Response(success_response('Vendor detail.', VendorSerializer(vendor).data), status=200)

    def put(self, request, vendor_id):
        vendor = get_vendor_detail(organization=request.organization, vendor_id=vendor_id)
        serializer = VendorCreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        owner_user_id = data.pop('owner_user', None)
        if owner_user_id is not None:
            owner_user = _resolve_owner_user(organization=request.organization, owner_user_id=owner_user_id)
            if owner_user_id and owner_user is None:
                return Response(
                    error_response('Owner user must be a member of the organization.', 'invalid_owner'),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data['owner_user'] = owner_user
        vendor = VendorService.update_vendor(
            vendor=vendor, organization=request.organization, actor=request.user, **data
        )
        return Response(success_response('Vendor updated.', VendorSerializer(vendor).data), status=200)

    def patch(self, request, vendor_id):
        return self.put(request, vendor_id)


class VendorContactListCreateView(OrganizationContextMixin, APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [CanManageVendors()]
        return [IsOrganizationMember()]

    def get(self, request, vendor_id):
        vendor = get_vendor_detail(organization=request.organization, vendor_id=vendor_id)
        contacts = VendorContact.objects.filter(vendor=vendor).order_by('name')
        serializer = VendorContactSerializer(contacts, many=True)
        return Response(success_response('Vendor contacts retrieved.', serializer.data), status=200)

    def post(self, request, vendor_id):
        vendor = get_vendor_detail(organization=request.organization, vendor_id=vendor_id)
        serializer = VendorContactCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = VendorContact.objects.create(vendor=vendor, **serializer.validated_data)
        return Response(
            success_response('Vendor contact created.', VendorContactSerializer(contact).data),
            status=status.HTTP_201_CREATED,
        )


class VendorTimelineView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request, vendor_id):
        get_vendor_detail(organization=request.organization, vendor_id=vendor_id)
        events = get_vendor_timeline(organization=request.organization, vendor_id=vendor_id)
        data = [
            {
                'id': str(event.id),
                'action': event.action,
                'entity_type': event.entity_type,
                'entity_id': str(event.entity_id),
                'actor_user_id': str(event.actor_user_id) if event.actor_user_id else None,
                'created_at': event.created_at,
                'old_data': event.old_data_json,
                'new_data': event.new_data_json,
            }
            for event in events
        ]
        return Response(success_response('Vendor timeline.', data), status=200)


class VendorStatusSummaryView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request, vendor_id):
        get_vendor_detail(organization=request.organization, vendor_id=vendor_id)
        data = get_vendor_status_summary(organization=request.organization, vendor_id=vendor_id)
        return Response(success_response('Vendor status summary.', data), status=200)
