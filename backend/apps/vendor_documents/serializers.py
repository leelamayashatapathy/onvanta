from __future__ import annotations

from rest_framework import serializers

from .models import VendorDocument


class VendorDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDocument
        fields = (
            'id',
            'vendor',
            'document_type',
            'file',
            'file_path',
            'original_name',
            'mime_type',
            'file_size',
            'checksum',
            'version',
            'issue_date',
            'expiry_date',
            'status',
            'verification_status',
            'verified_by',
            'verified_at',
            'rejection_reason',
            'supersedes_document',
            'uploaded_by',
            'uploaded_at',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class VendorDocumentUploadSerializer(serializers.Serializer):
    vendor_id = serializers.UUIDField()
    document_type_id = serializers.UUIDField()
    file = serializers.FileField()
    issue_date = serializers.DateField(required=False, allow_null=True)
    expiry_date = serializers.DateField(required=False, allow_null=True)


class VendorDocumentRejectSerializer(serializers.Serializer):
    rejection_reason = serializers.CharField()