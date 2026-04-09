from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import CanManageOnboarding, CanReviewOnboarding, IsOrganizationMember
from apps.api.responses import success_response
from apps.approvals.selectors import get_active_flow
from apps.approvals.services import ApprovalService
from apps.onboarding.selectors import (
    get_case_checklist,
    get_case_detail,
    list_blocked_cases,
    list_pending_cases,
)
from apps.onboarding.serializers import (
    OnboardingCaseSerializer,
    OnboardingCaseStartSerializer,
    OnboardingRequirementSerializer,
)
from apps.onboarding.services import OnboardingService
from apps.onboarding.validators import ensure_no_active_case
from apps.onboarding.models import OnboardingTemplate
from apps.vendors.selectors import get_vendor_detail


class OnboardingCaseStartView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOnboarding]

    def post(self, request):
        serializer = OnboardingCaseStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        vendor = get_vendor_detail(organization=request.organization, vendor_id=data['vendor_id'])
        template = OnboardingTemplate.objects.get(
            id=data['template_id'], organization=request.organization
        )
        ensure_no_active_case(vendor=vendor)
        case = OnboardingService.start_case(
            organization=request.organization, vendor=vendor, template=template, actor=request.user
        )
        return Response(
            success_response('Onboarding case started.', OnboardingCaseSerializer(case).data),
            status=status.HTTP_201_CREATED,
        )


class OnboardingCaseDetailView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request, case_id):
        case = get_case_detail(organization=request.organization, case_id=case_id)
        return Response(success_response('Onboarding case detail.', OnboardingCaseSerializer(case).data))


class OnboardingCaseChecklistView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request, case_id):
        checklist = get_case_checklist(organization=request.organization, case_id=case_id)
        serializer = OnboardingRequirementSerializer(checklist, many=True)
        return Response(success_response('Onboarding checklist.', serializer.data))


class OnboardingCaseSubmitView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOnboarding]

    def post(self, request, case_id):
        case = get_case_detail(organization=request.organization, case_id=case_id)
        case = OnboardingService.submit_for_review(
            case=case, organization=request.organization, actor=request.user
        )
        return Response(success_response('Onboarding case submitted.', OnboardingCaseSerializer(case).data))


class OnboardingCaseSubmitApprovalView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOnboarding]

    def post(self, request, case_id):
        case = get_case_detail(organization=request.organization, case_id=case_id)
        case = OnboardingService.submit_for_approval(
            case=case, organization=request.organization, actor=request.user
        )
        if case.status == 'approval_pending':
            flow = get_active_flow(organization=request.organization, scope='onboarding')
            ApprovalService.submit_case(
                organization=request.organization, onboarding_case=case, flow=flow, actor=request.user
            )
        return Response(success_response('Onboarding sent for approval.', OnboardingCaseSerializer(case).data))


class OnboardingPendingQueueView(OrganizationContextMixin, APIView):
    permission_classes = [CanReviewOnboarding]

    def get(self, request):
        queryset = list_pending_cases(organization=request.organization)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OnboardingCaseSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Pending onboarding cases.', serializer.data, metadata))


class OnboardingBlockedCasesView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOnboarding]

    def get(self, request):
        queryset = list_blocked_cases(organization=request.organization)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OnboardingCaseSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Blocked onboarding cases.', serializer.data, metadata))