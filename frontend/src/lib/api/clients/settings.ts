import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { DocumentType, OnboardingTemplate } from "../../../types";

export interface CreateDocumentTypePayload {
  code: string;
  name: string;
  description?: string;
  category?: string;
  is_mandatory?: boolean;
  has_expiry?: boolean;
  expiry_warning_days?: number;
  criticality: DocumentType["criticality"];
  applies_to_vendor_type?: string;
  allowed_extensions?: string[];
  max_file_size_mb?: number;
}

export interface CreateTemplatePayload {
  name: string;
  applies_to_vendor_category?: string;
  active?: boolean;
}

export async function fetchDocumentTypes() {
  const response = await apiClient.get<ApiResponse<DocumentType[]>>("/document-types/");
  return unwrapResponse(response);
}

export async function fetchTemplates() {
  const response = await apiClient.get<ApiResponse<OnboardingTemplate[]>>("/onboarding-templates/");
  return unwrapResponse(response);
}

export async function createDocumentType(payload: CreateDocumentTypePayload) {
  const response = await apiClient.post<ApiResponse<DocumentType>>("/document-types/", payload);
  return unwrapResponse(response);
}

export async function createTemplate(payload: CreateTemplatePayload) {
  const response = await apiClient.post<ApiResponse<OnboardingTemplate>>("/onboarding-templates/", payload);
  return unwrapResponse(response);
}
