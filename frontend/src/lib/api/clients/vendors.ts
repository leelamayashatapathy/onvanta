import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { Vendor } from "../../../types";

export interface CreateVendorPayload {
  vendor_code: string;
  legal_name: string;
  display_name: string;
  vendor_type?: string;
  category?: string;
  risk_level?: Vendor["risk_level"];
  owner_user?: string | null;
  notes?: string;
}

export async function fetchVendors() {
  const response = await apiClient.get<ApiResponse<Vendor[]>>("/vendors/");
  return unwrapResponse(response);
}

export async function fetchVendorById(vendorId: string) {
  const response = await apiClient.get<ApiResponse<Vendor>>(`/vendors/${vendorId}/`);
  return unwrapResponse(response);
}

export async function createVendor(payload: CreateVendorPayload) {
  const response = await apiClient.post<ApiResponse<Vendor>>("/vendors/", payload);
  return unwrapResponse(response);
}
