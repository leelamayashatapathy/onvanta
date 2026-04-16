from django.urls import path

from .views import (
    VendorContactListCreateView,
    VendorDetailView,
    VendorListCreateView,
    VendorStatusSummaryView,
    VendorTimelineView,
)

urlpatterns = [
    path('', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('<uuid:vendor_id>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('<uuid:vendor_id>/timeline/', VendorTimelineView.as_view(), name='vendor-timeline'),
    path('<uuid:vendor_id>/status-summary/', VendorStatusSummaryView.as_view(), name='vendor-status-summary'),
    path('<uuid:vendor_id>/contacts/', VendorContactListCreateView.as_view(), name='vendor-contacts'),
]
