import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { OrganizationDetail } from "../../../types";

export async function fetchOrganizationDetail() {
  const response = await apiClient.get<ApiResponse<OrganizationDetail>>("/organizations/detail/");
  return unwrapResponse(response);
}
