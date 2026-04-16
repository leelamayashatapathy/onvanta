from django.urls import path

from .views import VendorDocumentListView

urlpatterns = [
    path('<uuid:vendor_id>/documents/', VendorDocumentListView.as_view(), name='vendor-document-list'),
]
