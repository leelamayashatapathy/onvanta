from django.contrib import admin

from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ('organization', 'entity_type', 'action', 'actor_user', 'created_at')
    list_filter = ('action', 'entity_type')
    search_fields = ('entity_type', 'entity_id', 'actor_user__email')