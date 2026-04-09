from __future__ import annotations

from rest_framework import serializers

from .models import ApprovalDecision, ApprovalFlow, ApprovalStep


class ApprovalFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalFlow
        fields = ('id', 'name', 'scope', 'active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ApprovalFlowCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    scope = serializers.CharField(max_length=50)
    active = serializers.BooleanField(default=True)


class ApprovalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalStep
        fields = (
            'id',
            'flow',
            'step_order',
            'role_required',
            'explicit_user',
            'decision_type',
            'active',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class ApprovalStepCreateSerializer(serializers.Serializer):
    step_order = serializers.IntegerField(min_value=1)
    role_required = serializers.CharField(max_length=50)
    explicit_user = serializers.UUIDField(required=False, allow_null=True)
    decision_type = serializers.CharField(max_length=20, required=False, default='single')
    active = serializers.BooleanField(default=True)


class ApprovalDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalDecision
        fields = (
            'id',
            'onboarding_case',
            'approval_step',
            'decision',
            'decided_by',
            'decided_at',
            'comments',
            'created_at',
            'updated_at',
        )
        read_only_fields = fields


class ApprovalDecisionActionSerializer(serializers.Serializer):
    comments = serializers.CharField(required=False, allow_blank=True)