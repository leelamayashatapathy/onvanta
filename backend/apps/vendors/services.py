from __future__ import annotations

from apps.auditlog.services import AuditService
from apps.organizations.models import Organization

from .models import Vendor
from .validators import validate_vendor_ownership


class VendorService:
    @staticmethod
    def create_vendor(*, organization: Organization, actor, **data) -> Vendor:
        vendor = Vendor.objects.create(organization=organization, **data)
        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='Vendor',
            entity_id=vendor.id,
            action='vendor_created',
            source='api',
            new_data={'vendor_id': str(vendor.id), 'name': vendor.display_name},
        )
        return vendor

    @staticmethod
    def update_vendor(*, vendor: Vendor, organization: Organization, actor, **data) -> Vendor:
        validate_vendor_ownership(vendor=vendor, organization=organization)
        old = {
            'legal_name': vendor.legal_name,
            'display_name': vendor.display_name,
            'category': vendor.category,
            'vendor_type': vendor.vendor_type,
            'risk_level': vendor.risk_level,
            'notes': vendor.notes,
        }
        for field, value in data.items():
            setattr(vendor, field, value)
        vendor.save(update_fields=list(data.keys()) + ['updated_at'])
        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='Vendor',
            entity_id=vendor.id,
            action='vendor_updated',
            source='api',
            old_data=old,
            new_data=data,
        )
        return vendor

    @staticmethod
    def assign_owner(*, vendor: Vendor, organization: Organization, owner_user, actor) -> Vendor:
        validate_vendor_ownership(vendor=vendor, organization=organization)
        vendor.owner_user = owner_user
        vendor.save(update_fields=['owner_user', 'updated_at'])
        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='Vendor',
            entity_id=vendor.id,
            action='vendor_owner_assigned',
            source='api',
            new_data={'owner_user_id': str(owner_user.id) if owner_user else None},
        )
        return vendor

    @staticmethod
    def change_operational_status(*, vendor: Vendor, organization: Organization, status: str, actor) -> Vendor:
        validate_vendor_ownership(vendor=vendor, organization=organization)
        vendor.operational_status = status
        vendor.save(update_fields=['operational_status', 'updated_at'])
        AuditService.log_event(
            organization=organization,
            actor_user=actor,
            actor_type='user',
            entity_type='Vendor',
            entity_id=vendor.id,
            action='vendor_operational_status_changed',
            source='api',
            new_data={'operational_status': status},
        )
        return vendor
