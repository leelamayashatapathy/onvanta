from django.urls import path

from .views import TaskListCreateView, TaskStatusUpdateView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<uuid:task_id>/complete/', TaskStatusUpdateView.as_view(), name='task-complete'),
]
