from __future__ import annotations

from rest_framework import serializers

from .models import ReminderSchedule


class ReminderScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderSchedule
        fields = (
            'id',
            'vendor_document',
            'reminder_type',
            'scheduled_for',
            'sent_at',
            'status',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class ExpiryQuerySerializer(serializers.Serializer):
    days = serializers.IntegerField(required=False, min_value=1, max_value=365)