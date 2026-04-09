from __future__ import annotations

import uuid

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, ValidationError

from .models import Organization, OrganizationMember
from .enums import OrganizationMemberStatus


def resolve_organization_context(request):
    if not request.user or not request.user.is_authenticated:
        raise NotAuthenticated('Authentication required.')

    org_id = request.headers.get('X-ORG-ID') or request.query_params.get('org_id')
    if not org_id:
        raise ValidationError({'org_id': 'Organization id is required via X-ORG-ID header or org_id.'})

    try:
        org_uuid = uuid.UUID(str(org_id))
    except ValueError as exc:
        raise ValidationError({'org_id': 'Invalid organization id.'}) from exc

    try:
        organization = Organization.objects.get(id=org_uuid)
    except ObjectDoesNotExist as exc:
        raise ValidationError({'org_id': 'Organization not found.'}) from exc

    try:
        member = OrganizationMember.objects.get(user=request.user, organization=organization)
    except ObjectDoesNotExist as exc:
        raise PermissionDenied('You are not a member of this organization.') from exc

    if member.status != OrganizationMemberStatus.ACTIVE:
        raise PermissionDenied('Your organization membership is not active.')

    return organization, member