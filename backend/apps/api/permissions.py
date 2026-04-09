from __future__ import annotations

from apps.common.permissions import HasOrganizationRole
from apps.organizations.enums import OrganizationMemberRole


class IsOrganizationMember(HasOrganizationRole):
    required_roles: set[str] = set()


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
