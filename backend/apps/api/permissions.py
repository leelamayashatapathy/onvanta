from __future__ import annotations

from rest_framework.permissions import BasePermission

from apps.common.permissions import HasOrganizationRole
from apps.organizations.enums import OrganizationMemberRole


class IsOrganizationMember(HasOrganizationRole):
    required_roles: set[str] = set()


class IsPlatformAdmin(BasePermission):
    message = 'Platform admin access required.'

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.is_platform_admin)


class CanManageVendors(HasOrganizationRole):
    required_roles = {
        OrganizationMemberRole.ORG_ADMIN,
        OrganizationMemberRole.PROCUREMENT_MANAGER,
    }


class CanManageDocumentTypes(HasOrganizationRole):
    required_roles = {
        OrganizationMemberRole.ORG_ADMIN,
        OrganizationMemberRole.COMPLIANCE_MANAGER,
    }


class CanManageOnboardingTemplates(HasOrganizationRole):
    required_roles = {
        OrganizationMemberRole.ORG_ADMIN,
        OrganizationMemberRole.COMPLIANCE_MANAGER,
    }


class CanReviewDocuments(HasOrganizationRole):
    required_roles = {
        OrganizationMemberRole.ORG_ADMIN,
        OrganizationMemberRole.REVIEWER,
        OrganizationMemberRole.COMPLIANCE_MANAGER,
    }


class CanManageOnboarding(HasOrganizationRole):
    required_roles = {
        OrganizationMemberRole.ORG_ADMIN,
        OrganizationMemberRole.PROCUREMENT_MANAGER,
    }


class CanReviewOnboarding(HasOrganizationRole):
    required_roles = {
        OrganizationMemberRole.ORG_ADMIN,
        OrganizationMemberRole.REVIEWER,
        OrganizationMemberRole.APPROVER,
        OrganizationMemberRole.COMPLIANCE_MANAGER,
    }


class CanApproveOnboarding(HasOrganizationRole):
    required_roles = {
        OrganizationMemberRole.ORG_ADMIN,
        OrganizationMemberRole.APPROVER,
    }


class CanManageTasks(HasOrganizationRole):
    required_roles = {
        OrganizationMemberRole.ORG_ADMIN,
        OrganizationMemberRole.PROCUREMENT_MANAGER,
        OrganizationMemberRole.COMPLIANCE_MANAGER,
    }


class CanManageOrgSettings(HasOrganizationRole):
    required_roles = {OrganizationMemberRole.ORG_ADMIN}
