from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import CanManageOnboarding, IsOrganizationMember
from apps.api.responses import success_response
from apps.expiries.selectors import list_overdue_expiries, list_upcoming_expiries
from apps.expiries.serializers import ExpiryQuerySerializer


class UpcomingExpiriesView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request):
        serializer = ExpiryQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        days = serializer.validated_data.get('days', 30)
        queryset = list_upcoming_expiries(organization=request.organization, days=days)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        data = [
            {
                'document_id': str(doc.id),
                'vendor_id': str(doc.vendor_id),
                'vendor_name': doc.vendor.display_name,
                'document_type': doc.document_type.name,
                'expiry_date': str(doc.expiry_date),
            }
            for doc in page
        ]
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Upcoming expiries.', data, metadata), status=200)


class OverdueExpiriesView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request):
        queryset = list_overdue_expiries(organization=request.organization)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        data = [
            {
                'document_id': str(doc.id),
                'vendor_id': str(doc.vendor_id),
                'vendor_name': doc.vendor.display_name,
                'document_type': doc.document_type.name,
                'expiry_date': str(doc.expiry_date),
            }
            for doc in page
        ]
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Overdue expiries.', data, metadata), status=200)