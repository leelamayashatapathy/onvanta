from __future__ import annotations

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import IsOrganizationMember
from apps.api.responses import success_response
from apps.notifications.serializers import NotificationLogSerializer


class NotificationLogListView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request):
        queryset = request.organization.notification_logs.order_by('-created_at')
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = NotificationLogSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Notifications retrieved.', serializer.data, metadata), status=200)