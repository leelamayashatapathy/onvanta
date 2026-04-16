from __future__ import annotations

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import OrganizationContextMixin
from apps.api.permissions import IsOrganizationMember
from apps.api.responses import success_response
from apps.dashboard.selectors import (
    get_expiry_stats,
    get_org_summary,
    get_pending_approval_counts,
    get_pipeline_stats,
)


class DashboardSummaryView(OrganizationContextMixin, APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request):
        data = {
            'organization': get_org_summary(organization=request.organization),
            'pending_approvals': get_pending_approval_counts(organization=request.organization),
            'pipeline': get_pipeline_stats(organization=request.organization),
            'expiries': get_expiry_stats(organization=request.organization),
        }
        return Response(success_response('Dashboard summary.', data))
