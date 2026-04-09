from __future__ import annotations

from apps.organizations.models import Organization

from .models import AuditEvent


class AuditService:
    @staticmethod
    def log_event(
        *,
        organization: Organization,
        actor_user,
        actor_type: str,
        entity_type: str,
        entity_id,
        action: str,
        source: str,
        old_data: dict | None = None,
        new_data: dict | None = None,
    ) -> AuditEvent:
        return AuditEvent.objects.create(
            organization=organization,
            actor_user=actor_user,
            actor_type=actor_type,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            source=source,
            old_data_json=old_data or {},
            new_data_json=new_data or {},
        )
