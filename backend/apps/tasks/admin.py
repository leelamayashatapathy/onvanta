from django.contrib import admin

from .models import ActionTask


@admin.register(ActionTask)
class ActionTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'organization__name')