from django.contrib import admin

from .models import Organization, OrganizationMember


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'industry', 'size', 'timezone')
    search_fields = ('name', 'slug')


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('organization', 'user', 'role', 'status')
    list_filter = ('role', 'status')
    search_fields = ('organization__name', 'user__email')