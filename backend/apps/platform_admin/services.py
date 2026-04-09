from __future__ import annotations

from apps.organizations.enums import OrganizationMemberRole, OrganizationMemberStatus
from apps.organizations.models import Organization, OrganizationMember
from apps.organizations.services import OrganizationInviteService


class PlatformAdminOrganizationService:
    @staticmethod
    def invite_admin(*, organization: Organization, email: str, invited_by) -> dict:
        invite = OrganizationInviteService.create_invite(
            organization=organization,
            email=email,
            role=OrganizationMemberRole.ORG_ADMIN,
            invited_by=invited_by,
        )
        return {
            'invite_id': str(invite.id),
            'token': invite.token,
            'email': invite.email,
            'expires_at': invite.expires_at,
        }

    @staticmethod
    def update_organization_status(*, organization: Organization, status: str) -> Organization:
        organization.status = status
        organization.save(update_fields=['status', 'updated_at'])
        return organization


class PlatformAdminUserService:
    @staticmethod
    def activate_user(*, user) -> None:
        user.is_active = True
        user.save(update_fields=['is_active', 'updated_at'])

    @staticmethod
    def deactivate_user(*, user) -> None:
        user.is_active = False
        user.save(update_fields=['is_active', 'updated_at'])

    @staticmethod
    def set_platform_admin_flag(*, user, value: bool) -> None:
        user.is_platform_admin = value
        user.save(update_fields=['is_platform_admin', 'updated_at'])


def ensure_org_admin_member(*, organization: Organization, user) -> OrganizationMember:
    member, _ = OrganizationMember.objects.get_or_create(
        organization=organization,
        user=user,
        defaults={'role': OrganizationMemberRole.ORG_ADMIN, 'status': OrganizationMemberStatus.ACTIVE},
    )
    if member.status != OrganizationMemberStatus.ACTIVE:
        member.status = OrganizationMemberStatus.ACTIVE
        member.save(update_fields=['status', 'updated_at'])
    return member
