from __future__ import annotations

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import IsOrganizationMember
from apps.api.responses import success_response
from apps.auditlog.selectors import list_audit_events, list_vendor_related_events
from apps.auditlog.serializers import AuditEventSerializer
from apps.vendors.selectors import get_vendor_detail


class AuditEventListView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request):
        queryset = list_audit_events(organization=request.organization)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = AuditEventSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Audit events retrieved.', serializer.data, metadata), status=200)


class VendorAuditTimelineView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request, vendor_id):
        vendor = get_vendor_detail(organization=request.organization, vendor_id=vendor_id)
        queryset = list_vendor_related_events(organization=request.organization, vendor_id=vendor.id)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = AuditEventSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Vendor audit timeline retrieved.', serializer.data, metadata), status=200)