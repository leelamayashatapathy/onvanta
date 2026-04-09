from __future__ import annotations

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .enums import OrganizationInviteStatus
from .models import OrganizationInvite


def validate_invite_token(token: str) -> OrganizationInvite:
    if not token:
        raise ValidationError({'token': 'Invite token is required.'})

    invite = (
        OrganizationInvite.objects.select_related('organization')
        .filter(token=token)
        .first()
    )
    if not invite:
        raise ValidationError({'token': 'Invalid invite token.'})

    if invite.status != OrganizationInviteStatus.PENDING:
        raise ValidationError({'token': 'Invite token has already been used or is no longer valid.'})

    if invite.expires_at <= timezone.now():
        invite.status = OrganizationInviteStatus.EXPIRED
        invite.save(update_fields=['status', 'updated_at'])
        raise ValidationError({'token': 'Invite token has expired.'})

    return invite
