from django.contrib import admin

from .models import ApprovalDecision, ApprovalFlow, ApprovalStep


@admin.register(ApprovalFlow)
class ApprovalFlowAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'scope', 'active')
    list_filter = ('active', 'scope')
    search_fields = ('name', 'organization__name')


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ('flow', 'step_order', 'role_required', 'explicit_user', 'active')
    list_filter = ('active',)
    search_fields = ('flow__name',)


@admin.register(ApprovalDecision)
class ApprovalDecisionAdmin(admin.ModelAdmin):
    list_display = ('onboarding_case', 'approval_step', 'decision', 'decided_by', 'decided_at')
    list_filter = ('decision',)
    search_fields = ('onboarding_case__id',)