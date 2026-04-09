import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { ExpiryItem } from "../../../types";

export async function fetchUpcomingExpiries(days = 30) {
  const response = await apiClient.get<ApiResponse<ExpiryItem[]>>("/expiries/upcoming/", {
    params: { days },
  });
  return unwrapResponse(response);
}

export async function fetchOverdueExpiries() {
  const response = await apiClient.get<ApiResponse<ExpiryItem[]>>("/expiries/overdue/");
  return unwrapResponse(response);
}
