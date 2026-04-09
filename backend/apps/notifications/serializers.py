from __future__ import annotations

from rest_framework import serializers

from .models import NotificationLog


class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = (
            'id',
            'organization',
            'channel',
            'recipient',
            'template_code',
            'payload_json',
            'sent_at',
            'status',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')