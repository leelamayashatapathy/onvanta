from django.urls import path

from .views import (
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
    path('status/', SetupStatusView.as_view(), name='setup-status'),
    path('organization-profile/', SetupOrganizationProfileView.as_view(), name='setup-org-profile'),
    path('invite-members/', SetupInviteMembersView.as_view(), name='setup-invite-members'),
    path('vendor-categories/', SetupVendorCategoriesView.as_view(), name='setup-vendor-categories'),
    path('document-types/', SetupDocumentTypesView.as_view(), name='setup-document-types'),
    path('onboarding-templates/', SetupOnboardingTemplatesView.as_view(), name='setup-templates'),
    path('approval-flow/', SetupApprovalFlowView.as_view(), name='setup-approval-flow'),
    path('notification-settings/', SetupNotificationSettingsView.as_view(), name='setup-notifications'),
    path('complete/', SetupCompleteView.as_view(), name='setup-complete'),
]
