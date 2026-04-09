from __future__ import annotations

from apps.organizations.models import Organization

from .models import ActionTask


class TaskService:
    @staticmethod
    def create_task(*, organization: Organization, **data) -> ActionTask:
        return ActionTask.objects.create(organization=organization, **data)

    @staticmethod
    def mark_complete(*, task: ActionTask) -> ActionTask:
        task.status = 'completed'
        task.save(update_fields=['status', 'updated_at'])
        return task