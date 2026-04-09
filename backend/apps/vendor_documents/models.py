from __future__ import annotations

from django.db import models
from django.utils import timezone

from apps.common.models import TimeStampedUUIDModel
from apps.common.utils import safe_join_path
from apps.document_types.models import DocumentType
from apps.organizations.models import Organization
from apps.vendors.models import Vendor

from .enums import DocumentStatus, DocumentVerificationStatus


def vendor_document_upload_path(instance: 'VendorDocument', filename: str) -> str:
    date_part = timezone.now().strftime('%Y/%m/%d')
    return safe_join_path(
        'vendor_documents',
        str(instance.organization_id),
        str(instance.vendor_id),
        str(instance.document_type_id),
        date_part,
        filename,
    )


class VendorDocument(TimeStampedUUIDModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='vendor_documents'
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='documents')
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, related_name='vendor_documents'
    )
    file = models.FileField(upload_to=vendor_document_upload_path)
    file_path = models.CharField(max_length=500)
    original_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    file_size = models.PositiveIntegerField()
    checksum = models.CharField(max_length=128)
    version = models.PositiveIntegerField(default=1)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=DocumentStatus.choices, default=DocumentStatus.PENDING
    )
    verification_status = models.CharField(
        max_length=20, choices=DocumentVerificationStatus.choices, default=DocumentVerificationStatus.PENDING
    )
    verified_by = models.ForeignKey(
        'accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='verified_documents'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    supersedes_document = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='superseded_by'
    )
    uploaded_by = models.ForeignKey(
        'accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='uploaded_documents'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'vendor']),
            models.Index(fields=['organization', 'expiry_date']),
            models.Index(fields=['organization', 'created_at']),
        ]

    def __str__(self) -> str:
        return f'{self.vendor.display_name} - {self.document_type.name}'