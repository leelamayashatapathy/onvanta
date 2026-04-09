from __future__ import annotations

from rest_framework import serializers

from .models import Vendor, VendorContact


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            'id',
            'vendor_code',
            'legal_name',
            'display_name',
            'vendor_type',
            'category',
            'risk_level',
            'owner_user',
            'onboarding_status',
            'operational_status',
            'notes',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class VendorCreateUpdateSerializer(serializers.Serializer):
    vendor_code = serializers.CharField(max_length=50)
    legal_name = serializers.CharField(max_length=255)
    display_name = serializers.CharField(max_length=255)
    vendor_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    category = serializers.CharField(max_length=100, required=False, allow_blank=True)
    risk_level = serializers.ChoiceField(choices=Vendor._meta.get_field('risk_level').choices, required=False)
    owner_user = serializers.UUIDField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class VendorContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorContact
        fields = (
            'id',
            'vendor',
            'name',
            'email',
            'phone',
            'designation',
            'is_primary',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class VendorContactCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    designation = serializers.CharField(max_length=100, required=False, allow_blank=True)
    is_primary = serializers.BooleanField(default=False)