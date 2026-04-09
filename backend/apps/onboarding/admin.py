from django.contrib import admin

from .models import (
    OnboardingCase,
    OnboardingRequirement,
    OnboardingTemplate,
    OnboardingTemplateRequirement,
)


@admin.register(OnboardingTemplate)
class OnboardingTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'applies_to_vendor_category', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'organization__name')


@admin.register(OnboardingTemplateRequirement)
class OnboardingTemplateRequirementAdmin(admin.ModelAdmin):
    list_display = ('template', 'document_type', 'required', 'sequence', 'review_required')
    list_filter = ('required', 'review_required')
    search_fields = ('template__name', 'document_type__name')


@admin.register(OnboardingCase)
class OnboardingCaseAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'organization', 'status', 'current_stage', 'progress_percent')
    list_filter = ('status',)
    search_fields = ('vendor__display_name', 'organization__name')


@admin.register(OnboardingRequirement)
class OnboardingRequirementAdmin(admin.ModelAdmin):
    list_display = ('case', 'document_type', 'required', 'submitted', 'verified', 'status')
    list_filter = ('required', 'submitted', 'verified', 'status')
    search_fields = ('case__id', 'document_type__name')