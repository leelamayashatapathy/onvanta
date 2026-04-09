from __future__ import annotations

from apps.organizations.utils import resolve_organization_context


class OrganizationContextMixin:
    def initial(self, request, *args, **kwargs):
        organization, member = resolve_organization_context(request)
        request.organization = organization
        request.organization_member = member
        return super().initial(request, *args, **kwargs)