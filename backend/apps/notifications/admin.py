from django.contrib import admin

from .models import NotificationLog


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('channel', 'recipient', 'template_code', 'status', 'sent_at')
    list_filter = ('status', 'channel')
    search_fields = ('recipient', 'template_code')