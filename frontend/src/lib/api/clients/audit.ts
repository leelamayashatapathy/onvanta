import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { AuditEvent } from "../../../types";

export async function fetchAuditEvents() {
  const response = await apiClient.get<ApiResponse<AuditEvent[]>>("/audit/events/");
  return unwrapResponse(response);
}
