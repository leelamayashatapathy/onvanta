from __future__ import annotations

import uuid

from django.db import models


class AuditEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        'organizations.Organization', on_delete=models.CASCADE, related_name='audit_events'
    )
    actor_user = models.ForeignKey(
        'accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_events'
    )
    actor_type = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=100)
    entity_id = models.UUIDField()
    action = models.CharField(max_length=100)
    source = models.CharField(max_length=50)
    old_data_json = models.JSONField(default=dict, blank=True)
    new_data_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['organization', 'action']),
            models.Index(fields=['entity_type', 'entity_id']),
        ]

    def __str__(self) -> str:
        return f'{self.entity_type}:{self.entity_id} {self.action}'
