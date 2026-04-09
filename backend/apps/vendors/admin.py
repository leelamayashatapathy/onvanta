from django.contrib import admin

from .models import Vendor, VendorContact


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'vendor_code',
        'organization',
        'onboarding_status',
        'operational_status',
        'risk_level',
    )
    list_filter = ('onboarding_status', 'operational_status', 'risk_level')
    search_fields = ('display_name', 'legal_name', 'vendor_code')


@admin.register(VendorContact)
class VendorContactAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'email', 'phone', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('name', 'email', 'vendor__display_name')