import { apiClient, unwrapResponse, type ApiResponse } from "../client";

export interface DashboardSummary {
  organization: {
    vendors_total: number;
    vendors_active: number;
    onboarding_active: number;
  };
  pending_approvals: {
    pending_approvals: number;
  };
  pipeline: Record<string, number>;
  expiries: {
    upcoming: number;
    overdue: number;
  };
}

export async function fetchDashboardSummary() {
  const response = await apiClient.get<ApiResponse<DashboardSummary>>("/dashboard/summary/");
  return unwrapResponse(response);
}
