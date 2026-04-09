from __future__ import annotations

import secrets
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from .enums import OrganizationInviteStatus, OrganizationMemberStatus
from .models import Organization, OrganizationInvite, OrganizationMember, OrganizationSetupProgress
from .validators import validate_invite_token


class OrganizationInviteService:
    @staticmethod
    def _generate_unique_token() -> str:
        for _ in range(5):
            token = secrets.token_urlsafe(32)
            if not OrganizationInvite.objects.filter(token=token).exists():
                return token
        raise RuntimeError('Unable to generate unique invite token.')

    @staticmethod
    def create_invite(
        *,
        organization: Organization,
        email: str,
        role: str,
        invited_by=None,
        expires_in_hours: int = 72,
    ) -> OrganizationInvite:
        token = OrganizationInviteService._generate_unique_token()
        expires_at = timezone.now() + timedelta(hours=expires_in_hours)
        return OrganizationInvite.objects.create(
            organization=organization,
            email=email.lower(),
            role=role,
            token=token,
            invited_by=invited_by,
            expires_at=expires_at,
            status=OrganizationInviteStatus.PENDING,
        )

    @staticmethod
    def accept_invite(*, token: str) -> dict:
        invite = validate_invite_token(token)
        return {
            'organization_id': str(invite.organization_id),
            'organization_name': invite.organization.name,
            'email': invite.email,
            'role': invite.role,
            'expires_at': invite.expires_at,
        }

    @staticmethod
    @transaction.atomic
    def set_password_from_invite(*, token: str, password: str, first_name: str = '', last_name: str = '') -> dict:
        invite = validate_invite_token(token)

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            email=invite.email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True,
            },
        )
        if not created:
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.is_active = True
        user.set_password(password)
        user.save(update_fields=['first_name', 'last_name', 'is_active', 'password', 'updated_at'])

        member, _ = OrganizationMember.objects.get_or_create(
            organization=invite.organization,
            user=user,
            defaults={'role': invite.role, 'status': OrganizationMemberStatus.ACTIVE},
        )
        if member.status != OrganizationMemberStatus.ACTIVE:
            member.status = OrganizationMemberStatus.ACTIVE
            member.save(update_fields=['status', 'updated_at'])

        OrganizationSetupProgress.objects.get_or_create(organization=invite.organization)

        invite.status = OrganizationInviteStatus.ACCEPTED
        invite.accepted_at = timezone.now()
        invite.save(update_fields=['status', 'accepted_at', 'updated_at'])

        return {
            'user_id': str(user.id),
            'organization_id': str(invite.organization_id),
            'member_id': str(member.id),
        }


class OrganizationRegistrationService:
    @staticmethod
    def create_organization(*, name: str, industry: str = '', size: str = '', timezone: str = 'UTC') -> Organization:
        from django.utils.text import slugify

        return Organization.objects.create(
            name=name,
            slug=slugify(name),
            industry=industry,
            size=size,
            timezone=timezone,
        )
