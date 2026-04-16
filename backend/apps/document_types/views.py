from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import CanManageDocumentTypes, IsOrganizationMember
from apps.api.responses import success_response
from apps.document_types.selectors import get_document_type_detail, list_document_types
from apps.document_types.serializers import (
    DocumentTypeCreateUpdateSerializer,
    DocumentTypeSerializer,
)
from apps.document_types.services import DocumentTypeService


class DocumentTypeListCreateView(OrganizationContextMixin, APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [CanManageDocumentTypes()]
        return [IsOrganizationMember()]

    def get(self, request):
        queryset = list_document_types(organization=request.organization)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = DocumentTypeSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Document types retrieved.', serializer.data, metadata), status=200)

    def post(self, request):
        serializer = DocumentTypeCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document_type = DocumentTypeService.create_document_type(
            organization=request.organization, **serializer.validated_data
        )
        return Response(
            success_response('Document type created.', DocumentTypeSerializer(document_type).data),
            status=status.HTTP_201_CREATED,
        )


class DocumentTypeDetailView(OrganizationContextMixin, APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [CanManageDocumentTypes()]
        return [IsOrganizationMember()]

    def get(self, request, document_type_id):
        document_type = get_document_type_detail(
            organization=request.organization, document_type_id=document_type_id
        )
        return Response(
            success_response('Document type detail.', DocumentTypeSerializer(document_type).data),
            status=200,
        )

    def put(self, request, document_type_id):
        document_type = get_document_type_detail(
            organization=request.organization, document_type_id=document_type_id
        )
        serializer = DocumentTypeCreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        document_type = DocumentTypeService.update_document_type(
            document_type=document_type,
            organization=request.organization,
            **serializer.validated_data,
        )
        return Response(
            success_response('Document type updated.', DocumentTypeSerializer(document_type).data),
            status=200,
        )

    def patch(self, request, document_type_id):
        return self.put(request, document_type_id)
