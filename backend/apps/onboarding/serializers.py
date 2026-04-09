from __future__ import annotations

from rest_framework import serializers

from .models import OnboardingCase, OnboardingRequirement, OnboardingTemplate, OnboardingTemplateRequirement


class OnboardingTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingTemplate
        fields = (
            'id',
            'name',
            'applies_to_vendor_category',
            'active',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class OnboardingTemplateCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    applies_to_vendor_category = serializers.CharField(max_length=100, required=False, allow_blank=True)
    active = serializers.BooleanField(default=True)


class OnboardingTemplateRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingTemplateRequirement
        fields = (
            'id',
            'template',
            'document_type',
            'required',
            'sequence',
            'review_required',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class OnboardingTemplateRequirementCreateSerializer(serializers.Serializer):
    document_type = serializers.UUIDField()
    required = serializers.BooleanField(default=True)
    sequence = serializers.IntegerField(min_value=0, default=0)
    review_required = serializers.BooleanField(default=True)


class OnboardingTemplateRequirementUpdateSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    required = serializers.BooleanField(required=False)
    sequence = serializers.IntegerField(min_value=0, required=False)
    review_required = serializers.BooleanField(required=False)


class OnboardingCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingCase
        fields = (
            'id',
            'vendor',
            'template',
            'current_stage',
            'status',
            'progress_percent',
            'started_at',
            'submitted_at',
            'completed_at',
            'blocked_reason',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class OnboardingCaseStartSerializer(serializers.Serializer):
    vendor_id = serializers.UUIDField()
    template_id = serializers.UUIDField()


class OnboardingRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingRequirement
        fields = (
            'id',
            'case',
            'document_type',
            'required',
            'submitted',
            'verified',
            'current_document',
            'due_date',
            'status',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
