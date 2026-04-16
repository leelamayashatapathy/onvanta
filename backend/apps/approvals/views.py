from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.pagination import StandardResultsPagination
from apps.api.permissions import CanApproveOnboarding, CanManageOnboarding, CanReviewOnboarding
from apps.api.responses import success_response
from apps.approvals.models import ApprovalDecision, ApprovalFlow, ApprovalStep
from apps.approvals.selectors import (
    get_flow_detail,
    list_case_decisions,
    list_flows,
    list_pending_approvals,
)
from apps.approvals.serializers import (
    ApprovalDecisionActionSerializer,
    ApprovalDecisionSerializer,
    ApprovalFlowCreateUpdateSerializer,
    ApprovalFlowSerializer,
    ApprovalStepCreateSerializer,
    ApprovalStepSerializer,
)
from apps.approvals.services import ApprovalService


class ApprovalFlowListCreateView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOnboarding]

    def get(self, request):
        queryset = list_flows(organization=request.organization)
        serializer = ApprovalFlowSerializer(queryset, many=True)
        return Response(success_response('Approval flows.', serializer.data), status=200)

    def post(self, request):
        serializer = ApprovalFlowCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        flow = ApprovalFlow.objects.create(organization=request.organization, **serializer.validated_data)
        return Response(
            success_response('Approval flow created.', ApprovalFlowSerializer(flow).data),
            status=status.HTTP_201_CREATED,
        )


class ApprovalFlowDetailView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOnboarding]

    def get(self, request, flow_id):
        flow = get_flow_detail(organization=request.organization, flow_id=flow_id)
        return Response(success_response('Approval flow detail.', ApprovalFlowSerializer(flow).data), status=200)

    def put(self, request, flow_id):
        flow = get_flow_detail(organization=request.organization, flow_id=flow_id)
        serializer = ApprovalFlowCreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        for field, value in serializer.validated_data.items():
            setattr(flow, field, value)
        flow.save(update_fields=list(serializer.validated_data.keys()) + ['updated_at'])
        return Response(success_response('Approval flow updated.', ApprovalFlowSerializer(flow).data), status=200)


class ApprovalStepListCreateView(OrganizationContextMixin, APIView):
    permission_classes = [CanManageOnboarding]

    def get(self, request, flow_id):
        flow = get_flow_detail(organization=request.organization, flow_id=flow_id)
        serializer = ApprovalStepSerializer(flow.steps.order_by('step_order'), many=True)
        return Response(success_response('Approval steps.', serializer.data), status=200)

    def post(self, request, flow_id):
        flow = get_flow_detail(organization=request.organization, flow_id=flow_id)
        serializer = ApprovalStepCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        step = ApprovalStep.objects.create(flow=flow, **serializer.validated_data)
        return Response(success_response('Approval step created.', ApprovalStepSerializer(step).data), status=201)


class ApprovalQueueView(OrganizationContextMixin, APIView):
    permission_classes = [CanReviewOnboarding]

    def get(self, request):
        queryset = list_pending_approvals(organization=request.organization)
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ApprovalDecisionSerializer(page, many=True)
        metadata = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }
        return Response(success_response('Approval queue.', serializer.data, metadata), status=200)


class ApprovalDecisionApproveView(OrganizationContextMixin, APIView):
    permission_classes = [CanApproveOnboarding]

    def post(self, request, decision_id):
        serializer = ApprovalDecisionActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        decision = ApprovalDecision.objects.select_related('onboarding_case', 'approval_step').get(
            id=decision_id, organization=request.organization
        )
        decision = ApprovalService.approve_step(
            decision=decision,
            organization=request.organization,
            actor=request.user,
            actor_role=request.organization_member.role,
            comments=serializer.validated_data.get('comments', ''),
        )
        return Response(
            success_response('Approval decision approved.', ApprovalDecisionSerializer(decision).data),
            status=status.HTTP_200_OK,
        )


class ApprovalDecisionRejectView(OrganizationContextMixin, APIView):
    permission_classes = [CanApproveOnboarding]

    def post(self, request, decision_id):
        serializer = ApprovalDecisionActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        decision = ApprovalDecision.objects.select_related('onboarding_case', 'approval_step').get(
            id=decision_id, organization=request.organization
        )
        decision = ApprovalService.reject_step(
            decision=decision,
            organization=request.organization,
            actor=request.user,
            actor_role=request.organization_member.role,
            comments=serializer.validated_data.get('comments', ''),
        )
        return Response(
            success_response('Approval decision rejected.', ApprovalDecisionSerializer(decision).data),
            status=status.HTTP_200_OK,
        )


class CaseApprovalHistoryView(OrganizationContextMixin, APIView):
    permission_classes = [CanReviewOnboarding]

    def get(self, request, case_id):
        case = request.organization.onboarding_cases.get(id=case_id)
        queryset = list_case_decisions(organization=request.organization, case_id=case.id)
        serializer = ApprovalDecisionSerializer(queryset, many=True)
        return Response(success_response('Approval history.', serializer.data), status=200)
