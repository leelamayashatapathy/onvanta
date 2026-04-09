import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { OnboardingCase, OnboardingRequirement } from "../../../types";

export async function fetchOnboardingCases() {
  const response = await apiClient.get<ApiResponse<OnboardingCase[]>>("/onboarding/cases/pending/");
  return unwrapResponse(response);
}

export async function fetchOnboardingCase(caseId: string) {
  const response = await apiClient.get<ApiResponse<OnboardingCase>>(`/onboarding/cases/${caseId}/`);
  return unwrapResponse(response);
}

export async function fetchOnboardingChecklist(caseId: string) {
  const response = await apiClient.get<ApiResponse<OnboardingRequirement[]>>(
    `/onboarding/cases/${caseId}/checklist/`
  );
  return unwrapResponse(response);
}

export async function submitOnboardingCase(caseId: string) {
  const response = await apiClient.post<ApiResponse<OnboardingCase>>(
    `/onboarding/cases/${caseId}/submit-approval/`
  );
  return unwrapResponse(response);
}

export async function startOnboardingCase(payload: { vendor_id: string; template_id: string }) {
  const response = await apiClient.post<ApiResponse<OnboardingCase>>("/onboarding/cases/start/", payload);
  return unwrapResponse(response);
}
