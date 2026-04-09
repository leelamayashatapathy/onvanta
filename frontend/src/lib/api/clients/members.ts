import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { OrganizationMember, UserRole } from "../../../types";

export async function fetchMembers() {
  const response = await apiClient.get<ApiResponse<OrganizationMember[]>>("/organizations/members/");
  return unwrapResponse(response);
}

export async function updateMemberRole(memberId: string, role: UserRole) {
  const response = await apiClient.post<ApiResponse<{ id: string; role: UserRole }>>(
    `/organizations/members/${memberId}/role/`,
    { role }
  );
  return unwrapResponse(response);
}
