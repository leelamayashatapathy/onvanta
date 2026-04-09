from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import CanManageVendors, CanReviewDocuments, IsOrganizationMember
from apps.api.responses import success_response
from apps.document_types.selectors import get_document_type_detail
from apps.vendors.selectors import get_vendor_detail
from apps.vendor_documents.selectors import get_document_detail, list_vendor_documents
from apps.vendor_documents.serializers import (
    VendorDocumentRejectSerializer,
    VendorDocumentSerializer,
    VendorDocumentUploadSerializer,
)
from apps.vendor_documents.services import DocumentService


class VendorDocumentUploadView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageVendors]

    def post(self, request):
        serializer = VendorDocumentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        vendor = get_vendor_detail(organization=request.organization, vendor_id=data['vendor_id'])
        document_type = get_document_type_detail(
            organization=request.organization, document_type_id=data['document_type_id']
        )
        document = DocumentService.upload_document(
            organization=request.organization,
            vendor=vendor,
            document_type=document_type,
            file_obj=data['file'],
            issue_date=data.get('issue_date'),
            expiry_date=data.get('expiry_date'),
            uploaded_by=request.user,
        )
        return Response(
            success_response('Document uploaded.', VendorDocumentSerializer(document).data),
            status=status.HTTP_201_CREATED,
        )


class VendorDocumentListView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request, vendor_id):
        queryset = list_vendor_documents(organization=request.organization, vendor_id=vendor_id)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = VendorDocumentSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Documents retrieved.', serializer.data, metadata), status=200)


class VendorDocumentDetailView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request, document_id):
        document = get_document_detail(organization=request.organization, document_id=document_id)
        return Response(
            success_response('Document detail.', VendorDocumentSerializer(document).data), status=200
        )


class VendorDocumentReviewView(OrganizationContextMixin, APIView):
    permission_classes = [CanReviewDocuments]

    def post(self, request, document_id):
        document = get_document_detail(organization=request.organization, document_id=document_id)
        document = DocumentService.mark_under_review(
            document=document, organization=request.organization, actor=request.user
        )
        return Response(
            success_response('Document marked under review.', VendorDocumentSerializer(document).data),
            status=200,
        )


class VendorDocumentApproveView(OrganizationContextMixin, APIView):
    permission_classes = [CanReviewDocuments]

    def post(self, request, document_id):
        document = get_document_detail(organization=request.organization, document_id=document_id)
        document = DocumentService.approve_document(
            document=document, organization=request.organization, actor=request.user
        )
        return Response(
            success_response('Document approved.', VendorDocumentSerializer(document).data), status=200
        )


class VendorDocumentRejectView(OrganizationContextMixin, APIView):
    permission_classes = [CanReviewDocuments]

    def post(self, request, document_id):
        serializer = VendorDocumentRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = get_document_detail(organization=request.organization, document_id=document_id)
        document = DocumentService.reject_document(
            document=document,
            organization=request.organization,
            actor=request.user,
            rejection_reason=serializer.validated_data['rejection_reason'],
        )
        return Response(
            success_response('Document rejected.', VendorDocumentSerializer(document).data), status=200
        )