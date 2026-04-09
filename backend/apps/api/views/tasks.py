from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import CanManageTasks, IsOrganizationMember
from apps.api.responses import success_response
from apps.tasks.serializers import ActionTaskCreateSerializer, ActionTaskSerializer
from apps.tasks.services import TaskService


class TaskListCreateView(OrganizationContextMixin, APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [CanManageTasks()]
        return [IsOrganizationMember()]

    def get(self, request):
        queryset = request.organization.tasks.select_related('vendor', 'onboarding_case').order_by('-created_at')
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ActionTaskSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Tasks retrieved.', serializer.data, metadata), status=200)

    def post(self, request):
        serializer = ActionTaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = TaskService.create_task(organization=request.organization, **serializer.validated_data)
        return Response(
            success_response('Task created.', ActionTaskSerializer(task).data),
            status=status.HTTP_201_CREATED,
        )


class TaskStatusUpdateView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageTasks]

    def post(self, request, task_id):
        task = request.organization.tasks.get(id=task_id)
        task = TaskService.mark_complete(task=task)
        return Response(success_response('Task completed.', ActionTaskSerializer(task).data), status=200)