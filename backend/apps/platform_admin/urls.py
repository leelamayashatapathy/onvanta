from django.urls import path

from .views import (
    PlatformAdminDashboardView,
    PlatformAdminInviteOrgAdminView,
    PlatformAdminOrganizationCreateView,
    PlatformAdminOrganizationDetailView,
    PlatformAdminOrganizationListView,
    PlatformAdminOrganizationStatusUpdateView,
)

urlpatterns = [
    path('dashboard/', PlatformAdminDashboardView.as_view(), name='platform-dashboard'),
    path('organizations/', PlatformAdminOrganizationListView.as_view(), name='platform-orgs'),
    path(
        'organizations/<uuid:org_id>/',
        PlatformAdminOrganizationDetailView.as_view(),
        name='platform-org-detail',
    ),
    path(
        'organizations/<uuid:org_id>/status/',
        PlatformAdminOrganizationStatusUpdateView.as_view(),
        name='platform-org-status',
    ),
    path(
        'organizations/create/',
        PlatformAdminOrganizationCreateView.as_view(),
        name='platform-org-create',
    ),
    path(
        'organizations/<uuid:org_id>/invite-admin/',
        PlatformAdminInviteOrgAdminView.as_view(),
        name='platform-org-invite-admin',
    ),
]
