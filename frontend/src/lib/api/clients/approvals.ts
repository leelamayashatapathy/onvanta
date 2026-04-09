import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { ApprovalDecision, ApprovalFlow } from "../../../types";

export async function fetchApprovals() {
  const response = await apiClient.get<ApiResponse<ApprovalDecision[]>>("/approvals/queue/");
  return unwrapResponse(response);
}

export async function fetchApprovalHistory(caseId: string) {
  const response = await apiClient.get<ApiResponse<ApprovalDecision[]>>(
    `/approvals/cases/${caseId}/history/`
  );
  return unwrapResponse(response);
}

export async function approveDecision(decisionId: string, comments?: string) {
  const response = await apiClient.post<ApiResponse<ApprovalDecision>>(
    `/approvals/decisions/${decisionId}/approve/`,
    { comments }
  );
  return unwrapResponse(response);
}

export async function rejectDecision(decisionId: string, comments?: string) {
  const response = await apiClient.post<ApiResponse<ApprovalDecision>>(
    `/approvals/decisions/${decisionId}/reject/`,
    { comments }
  );
  return unwrapResponse(response);
}

export async function fetchApprovalFlows() {
  const response = await apiClient.get<ApiResponse<ApprovalFlow[]>>("/approvals/flows/");
  return unwrapResponse(response);
}

export async function createApprovalFlow(payload: { name: string; scope: string; active: boolean }) {
  const response = await apiClient.post<ApiResponse<ApprovalFlow>>("/approvals/flows/", payload);
  return unwrapResponse(response);
}
