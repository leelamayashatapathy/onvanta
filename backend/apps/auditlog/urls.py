from django.urls import path

from .views import AuditEventListView, VendorAuditTimelineView

urlpatterns = [
    path('events/', AuditEventListView.as_view(), name='audit-event-list'),
    path('vendors/<uuid:vendor_id>/timeline/', VendorAuditTimelineView.as_view(), name='vendor-audit-timeline'),
]
