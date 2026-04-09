from __future__ import annotations

from rest_framework import serializers

from .models import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = (
            'id',
            'code',
            'name',
            'description',
            'category',
            'is_mandatory',
            'has_expiry',
            'expiry_warning_days',
            'criticality',
            'applies_to_vendor_type',
            'allowed_extensions',
            'max_file_size_mb',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class DocumentTypeCreateUpdateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(max_length=100, required=False, allow_blank=True)
    is_mandatory = serializers.BooleanField(default=False)
    has_expiry = serializers.BooleanField(default=False)
    expiry_warning_days = serializers.IntegerField(required=False, min_value=1)
    criticality = serializers.ChoiceField(choices=DocumentType._meta.get_field('criticality').choices)
    applies_to_vendor_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    allowed_extensions = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    max_file_size_mb = serializers.IntegerField(required=False, min_value=1)