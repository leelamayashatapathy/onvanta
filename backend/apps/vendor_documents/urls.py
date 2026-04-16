from django.urls import path

from .views import (
    VendorDocumentApproveView,
    VendorDocumentDetailView,
    VendorDocumentRejectView,
    VendorDocumentReviewView,
    VendorDocumentUploadView,
)

urlpatterns = [
    path('upload/', VendorDocumentUploadView.as_view(), name='vendor-document-upload'),
    path('<uuid:document_id>/', VendorDocumentDetailView.as_view(), name='document-detail'),
    path('<uuid:document_id>/review/', VendorDocumentReviewView.as_view(), name='document-review'),
    path('<uuid:document_id>/approve/', VendorDocumentApproveView.as_view(), name='document-approve'),
    path('<uuid:document_id>/reject/', VendorDocumentRejectView.as_view(), name='document-reject'),
]
