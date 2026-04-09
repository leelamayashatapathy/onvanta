from __future__ import annotations

from rest_framework.permissions import BasePermission


class HasOrganizationRole(BasePermission):
    required_roles: set[str] = set()

    def has_permission(self, request, view) -> bool:
        member = getattr(request, 'organization_member', None)
        if not member:
            return False
        if not self.required_roles:
            return True
        return member.role in self.required_roles