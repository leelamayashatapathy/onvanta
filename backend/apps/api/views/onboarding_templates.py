from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import CanManageOnboardingTemplates, IsOrganizationMember
from apps.api.responses import success_response
from apps.document_types.selectors import get_document_type_detail
from apps.onboarding.selectors import get_template_detail, list_templates
from apps.onboarding.services import OnboardingTemplateService

from apps.onboarding.serializers import (
    OnboardingTemplateCreateUpdateSerializer,
    OnboardingTemplateRequirementCreateSerializer,
    OnboardingTemplateRequirementSerializer,
    OnboardingTemplateRequirementUpdateSerializer,
    OnboardingTemplateSerializer,
)


class OnboardingTemplateListCreateView(OrganizationContextMixin, APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [CanManageOnboardingTemplates()]
        return [IsOrganizationMember()]

    def get(self, request):
        queryset = list_templates(organization=request.organization)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OnboardingTemplateSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Templates retrieved.', serializer.data, metadata), status=200)

    def post(self, request):
        serializer = OnboardingTemplateCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template = OnboardingTemplateService.create_template(
            organization=request.organization, **serializer.validated_data
        )
        return Response(
            success_response('Template created.', OnboardingTemplateSerializer(template).data),
            status=status.HTTP_201_CREATED,
        )


class OnboardingTemplateDetailView(OrganizationContextMixin, APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [CanManageOnboardingTemplates()]
        return [IsOrganizationMember()]

    def get(self, request, template_id):
        template = get_template_detail(organization=request.organization, template_id=template_id)
        return Response(
            success_response('Template detail.', OnboardingTemplateSerializer(template).data),
            status=200,
        )

    def put(self, request, template_id):
        template = get_template_detail(organization=request.organization, template_id=template_id)
        serializer = OnboardingTemplateCreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        template = OnboardingTemplateService.update_template(
            template=template,
            organization=request.organization,
            **serializer.validated_data,
        )
        return Response(
            success_response('Template updated.', OnboardingTemplateSerializer(template).data),
            status=200,
        )


class OnboardingTemplateRequirementListCreateView(OrganizationContextMixin, APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [CanManageOnboardingTemplates()]
        return [IsOrganizationMember()]

    def get(self, request, template_id):
        template = get_template_detail(organization=request.organization, template_id=template_id)
        requirements = template.requirements.select_related('document_type').order_by('sequence')
        serializer = OnboardingTemplateRequirementSerializer(requirements, many=True)
        return Response(success_response('Template requirements retrieved.', serializer.data), status=200)

    def post(self, request, template_id):
        template = get_template_detail(organization=request.organization, template_id=template_id)
        serializer = OnboardingTemplateRequirementCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document_type = get_document_type_detail(
            organization=request.organization, document_type_id=serializer.validated_data['document_type']
        )
        requirement = OnboardingTemplateService.add_requirement(
            template=template,
            document_type=document_type,
            required=serializer.validated_data['required'],
            sequence=serializer.validated_data['sequence'],
            review_required=serializer.validated_data['review_required'],
        )
        return Response(
            success_response(
                'Template requirement created.',
                OnboardingTemplateRequirementSerializer(requirement).data,
            ),
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request, template_id):
        template = get_template_detail(organization=request.organization, template_id=template_id)
        updates = request.data.get('requirements', [])
        updated = []
        for item in updates:
            serializer = OnboardingTemplateRequirementUpdateSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            requirement = template.requirements.get(id=serializer.validated_data['id'])
            payload = {k: v for k, v in serializer.validated_data.items() if k != 'id'}
            requirement = OnboardingTemplateService.update_requirement(
                requirement=requirement,
                template=template,
                **payload,
            )
            updated.append(OnboardingTemplateRequirementSerializer(requirement).data)
        return Response(success_response('Template requirements updated.', updated), status=200)
