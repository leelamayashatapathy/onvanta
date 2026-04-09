from __future__ import annotations

from rest_framework import serializers

from .models import ActionTask


class ActionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionTask
        fields = (
            'id',
            'organization',
            'vendor',
            'onboarding_case',
            'task_type',
            'title',
            'description',
            'assigned_to',
            'due_date',
            'status',
            'priority',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class ActionTaskCreateSerializer(serializers.Serializer):
    vendor = serializers.UUIDField(required=False, allow_null=True)
    onboarding_case = serializers.UUIDField(required=False, allow_null=True)
    task_type = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    assigned_to = serializers.UUIDField(required=False, allow_null=True)
    due_date = serializers.DateField(required=False, allow_null=True)
    priority = serializers.ChoiceField(choices=ActionTask._meta.get_field('priority').choices)