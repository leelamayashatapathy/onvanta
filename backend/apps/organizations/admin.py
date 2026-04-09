from django.contrib import admin

from .models import Organization, OrganizationInvite, OrganizationMember, OrganizationSetupProgress


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'industry', 'size', 'timezone', 'status')
    search_fields = ('name', 'slug')


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('organization', 'user', 'role', 'status')
    list_filter = ('role', 'status')
    search_fields = ('organization__name', 'user__email')


@admin.register(OrganizationInvite)
class OrganizationInviteAdmin(admin.ModelAdmin):
    list_display = ('organization', 'email', 'role', 'status', 'expires_at')
    list_filter = ('status', 'role')
    search_fields = ('organization__name', 'email')


@admin.register(OrganizationSetupProgress)
class OrganizationSetupProgressAdmin(admin.ModelAdmin):
    list_display = ('organization', 'setup_completed')
    list_filter = ('setup_completed',)
