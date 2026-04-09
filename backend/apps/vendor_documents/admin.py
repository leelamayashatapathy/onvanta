from django.contrib import admin

from .models import VendorDocument


@admin.register(VendorDocument)
class VendorDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'vendor',
        'document_type',
        'organization',
        'status',
        'verification_status',
        'uploaded_at',
    )
    list_filter = ('status', 'verification_status')
    search_fields = ('vendor__display_name', 'document_type__name', 'organization__name')