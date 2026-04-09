import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { VendorDocument } from "../../../types";

export interface UploadDocumentPayload {
  vendor_id: string;
  document_type_id: string;
  issue_date?: string;
  expiry_date?: string;
  file: File;
}

export async function fetchVendorDocuments(vendorId: string) {
  const response = await apiClient.get<ApiResponse<VendorDocument[]>>(
    `/vendors/${vendorId}/documents/`
  );
  return unwrapResponse(response);
}

export async function fetchDocument(documentId: string) {
  const response = await apiClient.get<ApiResponse<VendorDocument>>(`/documents/${documentId}/`);
  return unwrapResponse(response);
}

export async function uploadDocument(payload: UploadDocumentPayload) {
  const formData = new FormData();
  formData.append("vendor_id", payload.vendor_id);
  formData.append("document_type_id", payload.document_type_id);
  if (payload.issue_date) {
    formData.append("issue_date", payload.issue_date);
  }
  if (payload.expiry_date) {
    formData.append("expiry_date", payload.expiry_date);
  }
  formData.append("file", payload.file);

  const response = await apiClient.post<ApiResponse<VendorDocument>>(
    "/documents/upload/",
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
    }
  );
  return unwrapResponse(response);
}

export async function approveDocument(documentId: string) {
  const response = await apiClient.post<ApiResponse<VendorDocument>>(
    `/documents/${documentId}/approve/`
  );
  return unwrapResponse(response);
}

export async function rejectDocument(documentId: string, rejection_reason: string) {
  const response = await apiClient.post<ApiResponse<VendorDocument>>(
    `/documents/${documentId}/reject/`,
    { rejection_reason }
  );
  return unwrapResponse(response);
}
