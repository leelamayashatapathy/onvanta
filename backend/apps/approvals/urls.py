from django.urls import path

from .views import (
    ApprovalDecisionApproveView,
    ApprovalDecisionRejectView,
    ApprovalFlowDetailView,
    ApprovalFlowListCreateView,
    ApprovalQueueView,
    ApprovalStepListCreateView,
    CaseApprovalHistoryView,
)

urlpatterns = [
    path('queue/', ApprovalQueueView.as_view(), name='approval-queue'),
    path('flows/', ApprovalFlowListCreateView.as_view(), name='approval-flow-list-create'),
    path('flows/<uuid:flow_id>/', ApprovalFlowDetailView.as_view(), name='approval-flow-detail'),
    path('flows/<uuid:flow_id>/steps/', ApprovalStepListCreateView.as_view(), name='approval-flow-steps'),
    path(
        'decisions/<uuid:decision_id>/approve/',
        ApprovalDecisionApproveView.as_view(),
        name='approval-decision-approve',
    ),
    path(
        'decisions/<uuid:decision_id>/reject/',
        ApprovalDecisionRejectView.as_view(),
        name='approval-decision-reject',
    ),
    path('cases/<uuid:case_id>/history/', CaseApprovalHistoryView.as_view(), name='approval-history'),
]
