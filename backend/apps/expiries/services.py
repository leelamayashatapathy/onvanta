from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.auditlog.services import AuditService
from apps.notifications.services import NotificationService
from apps.organizations.models import Organization
from apps.vendor_documents.enums import DocumentStatus, DocumentVerificationStatus
from apps.vendor_documents.models import VendorDocument
from apps.vendors.enums import VendorOperationalStatus

from .enums import ReminderStatus, ReminderType
from .models import ReminderSchedule


class ExpiryService:
    @staticmethod
    def scan_upcoming_expiries(*, organization: Organization) -> list[VendorDocument]:
        return list(
            VendorDocument.objects.filter(
                organization=organization,
                expiry_date__isnull=False,
                status=DocumentStatus.ACTIVE,
            )
        )

    @staticmethod
    def create_reminder_schedules(*, organization: Organization) -> int:
        documents = ExpiryService.scan_upcoming_expiries(organization=organization)
        created = 0
        for doc in documents:
            warning_days = doc.document_type.expiry_warning_days
            if not warning_days:
                continue
            scheduled_for = timezone.make_aware(
                timezone.datetime.combine(doc.expiry_date - timedelta(days=warning_days), timezone.datetime.min.time())
            )
            exists = ReminderSchedule.objects.filter(
                organization=organization,
                vendor_document=doc,
                reminder_type=ReminderType.EXPIRY_WARNING,
                scheduled_for=scheduled_for,
            ).exists()
            if exists:
                continue
            ReminderSchedule.objects.create(
                organization=organization,
                vendor_document=doc,
                reminder_type=ReminderType.EXPIRY_WARNING,
                scheduled_for=scheduled_for,
            )
            created += 1
        return created

    @staticmethod
    def mark_expired_documents(*, organization: Organization) -> int:
        today = timezone.now().date()
        expired_docs = VendorDocument.objects.filter(
            organization=organization,
            expiry_date__lt=today,
            status=DocumentStatus.ACTIVE,
        )
        count = expired_docs.update(
            status=DocumentStatus.EXPIRED, verification_status=DocumentVerificationStatus.EXPIRED
        )
        return count

    @staticmethod
    def restrict_vendor_if_required(*, organization: Organization) -> int:
        expired_critical = VendorDocument.objects.filter(
            organization=organization,
            status=DocumentStatus.EXPIRED,
            document_type__criticality='critical',
        ).select_related('vendor')
        updated = 0
        for doc in expired_critical:
            vendor = doc.vendor
            if vendor.operational_status != VendorOperationalStatus.RESTRICTED:
                vendor.operational_status = VendorOperationalStatus.RESTRICTED
                vendor.save(update_fields=['operational_status', 'updated_at'])
                AuditService.log_event(
                    organization=organization,
                    actor_user=None,
                    actor_type='system',
                    entity_type='Vendor',
                    entity_id=vendor.id,
                    action='vendor_restricted',
                    source='system',
                    new_data={'vendor_id': str(vendor.id), 'reason': 'critical_document_expired'},
                )
                updated += 1
        return updated

    @staticmethod
    def execute_reminders(*, organization: Organization) -> int:
        now = timezone.now()
        reminders = ReminderSchedule.objects.filter(
            organization=organization,
            status=ReminderStatus.SCHEDULED,
            scheduled_for__lte=now,
        ).select_related('vendor_document', 'vendor_document__vendor')
        sent_count = 0
        for reminder in reminders:
            NotificationService.send_reminder(organization=organization, reminder=reminder)
            reminder.status = ReminderStatus.SENT
            reminder.sent_at = timezone.now()
            reminder.save(update_fields=['status', 'sent_at', 'updated_at'])
            AuditService.log_event(
                organization=organization,
                actor_user=None,
                actor_type='system',
                entity_type='ReminderSchedule',
                entity_id=reminder.id,
                action='reminder_sent',
                source='system',
                new_data={'reminder_id': str(reminder.id)},
            )
            sent_count += 1
        return sent_count
