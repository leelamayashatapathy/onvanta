from django.urls import path

from .views.document_types import DocumentTypeDetailView, DocumentTypeListCreateView
from .views.audit import AuditEventListView, VendorAuditTimelineView
from .views.onboarding_cases import (
    OnboardingBlockedCasesView,
    OnboardingCaseChecklistView,
    OnboardingCaseDetailView,
    OnboardingCaseStartView,
    OnboardingCaseSubmitApprovalView,
    OnboardingCaseSubmitView,
    OnboardingPendingQueueView,
)
from .views.approvals import (
    ApprovalFlowDetailView,
    ApprovalFlowListCreateView,
    ApprovalStepListCreateView,
    ApprovalDecisionApproveView,
    ApprovalDecisionRejectView,
    ApprovalQueueView,
    CaseApprovalHistoryView,
)
from .views.expiries import OverdueExpiriesView, UpcomingExpiriesView
from .views.notifications import NotificationLogListView
from .views.tasks import TaskListCreateView, TaskStatusUpdateView
from .views.dashboard import DashboardSummaryView
from .views.auth import (
    AcceptInviteView,
    CurrentUserView,
    LoginView,
    RefreshView,
    SetPasswordFromInviteView,
)
from .views.organizations import (
    OrganizationCreateView,
    OrganizationDetailView,
    OrganizationMemberRoleUpdateView,
    OrganizationMembersView,
)
from .views.documents import (
    VendorDocumentApproveView,
    VendorDocumentDetailView,
    VendorDocumentListView,
    VendorDocumentRejectView,
    VendorDocumentReviewView,
    VendorDocumentUploadView,
)
from .views.onboarding_templates import (
    OnboardingTemplateDetailView,
    OnboardingTemplateListCreateView,
    OnboardingTemplateRequirementListCreateView,
)
from .views.vendors import (
    VendorContactListCreateView,
    VendorDetailView,
    VendorListCreateView,
    VendorStatusSummaryView,
    VendorTimelineView,
)
from .views.platform_admin import (
    PlatformAdminDashboardView,
    PlatformAdminOrganizationCreateView,
    PlatformAdminOrganizationDetailView,
    PlatformAdminOrganizationListView,
    PlatformAdminOrganizationStatusUpdateView,
    PlatformAdminInviteOrgAdminView,
)
from .views.setup import (
    SetupApprovalFlowView,
    SetupCompleteView,
    SetupDocumentTypesView,
    SetupInviteMembersView,
    SetupNotificationSettingsView,
    SetupOnboardingTemplatesView,
    SetupOrganizationProfileView,
    SetupStatusView,
    SetupVendorCategoriesView,
)

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<uuid:vendor_id>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('vendors/<uuid:vendor_id>/timeline/', VendorTimelineView.as_view(), name='vendor-timeline'),
    path(
        'vendors/<uuid:vendor_id>/status-summary/',
        VendorStatusSummaryView.as_view(),
        name='vendor-status-summary',
    ),
    path(
        'vendors/<uuid:vendor_id>/contacts/',
        VendorContactListCreateView.as_view(),
        name='vendor-contacts',
    ),
    path('document-types/', DocumentTypeListCreateView.as_view(), name='document-type-list-create'),
    path(
        'document-types/<uuid:document_type_id>/',
        DocumentTypeDetailView.as_view(),
        name='document-type-detail',
    ),
    path(
        'onboarding-templates/',
        OnboardingTemplateListCreateView.as_view(),
        name='onboarding-template-list-create',
    ),
    path(
        'onboarding-templates/<uuid:template_id>/',
        OnboardingTemplateDetailView.as_view(),
        name='onboarding-template-detail',
    ),
    path(
        'onboarding-templates/<uuid:template_id>/requirements/',
        OnboardingTemplateRequirementListCreateView.as_view(),
        name='onboarding-template-requirements',
    ),
    path('documents/upload/', VendorDocumentUploadView.as_view(), name='vendor-document-upload'),
    path('documents/<uuid:document_id>/', VendorDocumentDetailView.as_view(), name='document-detail'),
    path(
        'documents/<uuid:document_id>/review/',
        VendorDocumentReviewView.as_view(),
        name='document-review',
    ),
    path(
        'documents/<uuid:document_id>/approve/',
        VendorDocumentApproveView.as_view(),
        name='document-approve',
    ),
    path(
        'documents/<uuid:document_id>/reject/',
        VendorDocumentRejectView.as_view(),
        name='document-reject',
    ),
    path(
        'vendors/<uuid:vendor_id>/documents/',
        VendorDocumentListView.as_view(),
        name='vendor-document-list',
    ),
    path('audit/events/', AuditEventListView.as_view(), name='audit-event-list'),
    path(
        'audit/vendors/<uuid:vendor_id>/timeline/',
        VendorAuditTimelineView.as_view(),
        name='vendor-audit-timeline',
    ),
    path('onboarding/cases/start/', OnboardingCaseStartView.as_view(), name='onboarding-case-start'),
    path('onboarding/cases/<uuid:case_id>/', OnboardingCaseDetailView.as_view(), name='onboarding-case-detail'),
    path(
        'onboarding/cases/<uuid:case_id>/checklist/',
        OnboardingCaseChecklistView.as_view(),
        name='onboarding-case-checklist',
    ),
    path(
        'onboarding/cases/<uuid:case_id>/submit/',
        OnboardingCaseSubmitView.as_view(),
        name='onboarding-case-submit',
    ),
    path(
        'onboarding/cases/<uuid:case_id>/submit-approval/',
        OnboardingCaseSubmitApprovalView.as_view(),
        name='onboarding-case-submit-approval',
    ),
    path(
        'onboarding/cases/pending/',
        OnboardingPendingQueueView.as_view(),
        name='onboarding-case-pending',
    ),
    path(
        'onboarding/cases/blocked/',
        OnboardingBlockedCasesView.as_view(),
        name='onboarding-case-blocked',
    ),
    path('approvals/queue/', ApprovalQueueView.as_view(), name='approval-queue'),
    path('approvals/flows/', ApprovalFlowListCreateView.as_view(), name='approval-flow-list-create'),
    path(
        'approvals/flows/<uuid:flow_id>/',
        ApprovalFlowDetailView.as_view(),
        name='approval-flow-detail',
    ),
    path(
        'approvals/flows/<uuid:flow_id>/steps/',
        ApprovalStepListCreateView.as_view(),
        name='approval-flow-steps',
    ),
    path(
        'approvals/decisions/<uuid:decision_id>/approve/',
        ApprovalDecisionApproveView.as_view(),
        name='approval-decision-approve',
    ),
    path(
        'approvals/decisions/<uuid:decision_id>/reject/',
        ApprovalDecisionRejectView.as_view(),
        name='approval-decision-reject',
    ),
    path(
        'approvals/cases/<uuid:case_id>/history/',
        CaseApprovalHistoryView.as_view(),
        name='approval-history',
    ),
    path('expiries/upcoming/', UpcomingExpiriesView.as_view(), name='expiries-upcoming'),
    path('expiries/overdue/', OverdueExpiriesView.as_view(), name='expiries-overdue'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<uuid:task_id>/complete/', TaskStatusUpdateView.as_view(), name='task-complete'),
    path('notifications/', NotificationLogListView.as_view(), name='notification-list'),
    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', RefreshView.as_view(), name='auth-refresh'),
    path('auth/me/', CurrentUserView.as_view(), name='auth-me'),
    path('auth/accept-invite/', AcceptInviteView.as_view(), name='auth-accept-invite'),
    path('auth/set-password-from-invite/', SetPasswordFromInviteView.as_view(), name='auth-set-password-from-invite'),
    path('organizations/', OrganizationCreateView.as_view(), name='organization-create'),
    path('organizations/detail/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('organizations/members/', OrganizationMembersView.as_view(), name='organization-members'),
    path(
        'organizations/members/<uuid:member_id>/role/',
        OrganizationMemberRoleUpdateView.as_view(),
        name='organization-member-role',
    ),
    path('platform-admin/dashboard/', PlatformAdminDashboardView.as_view(), name='platform-dashboard'),
    path('platform-admin/organizations/', PlatformAdminOrganizationListView.as_view(), name='platform-orgs'),
    path(
        'platform-admin/organizations/<uuid:org_id>/',
        PlatformAdminOrganizationDetailView.as_view(),
        name='platform-org-detail',
    ),
    path(
        'platform-admin/organizations/<uuid:org_id>/status/',
        PlatformAdminOrganizationStatusUpdateView.as_view(),
        name='platform-org-status',
    ),
    path(
        'platform-admin/organizations/create/',
        PlatformAdminOrganizationCreateView.as_view(),
        name='platform-org-create',
    ),
    path(
        'platform-admin/organizations/<uuid:org_id>/invite-admin/',
        PlatformAdminInviteOrgAdminView.as_view(),
        name='platform-org-invite-admin',
    ),
    path('setup/status/', SetupStatusView.as_view(), name='setup-status'),
    path('setup/organization-profile/', SetupOrganizationProfileView.as_view(), name='setup-org-profile'),
    path('setup/invite-members/', SetupInviteMembersView.as_view(), name='setup-invite-members'),
    path('setup/vendor-categories/', SetupVendorCategoriesView.as_view(), name='setup-vendor-categories'),
    path('setup/document-types/', SetupDocumentTypesView.as_view(), name='setup-document-types'),
    path('setup/onboarding-templates/', SetupOnboardingTemplatesView.as_view(), name='setup-templates'),
    path('setup/approval-flow/', SetupApprovalFlowView.as_view(), name='setup-approval-flow'),
    path('setup/notification-settings/', SetupNotificationSettingsView.as_view(), name='setup-notifications'),
    path('setup/complete/', SetupCompleteView.as_view(), name='setup-complete'),
]
