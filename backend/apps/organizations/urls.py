from django.urls import path

from .views import (
    OrganizationCreateView,
    OrganizationDetailView,
    OrganizationMemberRoleUpdateView,
    OrganizationMembersView,
)

urlpatterns = [
    path('', OrganizationCreateView.as_view(), name='organization-create'),
    path('detail/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('members/', OrganizationMembersView.as_view(), name='organization-members'),
    path(
        'members/<uuid:member_id>/role/',
        OrganizationMemberRoleUpdateView.as_view(),
        name='organization-member-role',
    ),
]
