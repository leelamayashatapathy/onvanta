from django.contrib import admin

from .models import ReminderSchedule


@admin.register(ReminderSchedule)
class ReminderScheduleAdmin(admin.ModelAdmin):
    list_display = ('vendor_document', 'reminder_type', 'scheduled_for', 'status')
    list_filter = ('reminder_type', 'status')
    search_fields = ('vendor_document__id',)