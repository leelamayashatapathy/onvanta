from django.contrib import admin

from .models import DocumentType


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization', 'category', 'is_mandatory', 'has_expiry')
    list_filter = ('category', 'is_mandatory', 'has_expiry', 'criticality')
    search_fields = ('name', 'code', 'organization__name')