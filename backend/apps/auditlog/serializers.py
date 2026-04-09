from __future__ import annotations

from rest_framework import serializers

from .models import AuditEvent


class AuditEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditEvent
        fields = (
            'id',
            'organization',
            'actor_user',
            'actor_type',
            'entity_type',
            'entity_id',
            'action',
            'source',
            'old_data_json',
            'new_data_json',
            'created_at',
        )
        read_only_fields = fields