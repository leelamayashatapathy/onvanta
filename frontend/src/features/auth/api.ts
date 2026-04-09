import { apiClient, unwrapResponse, type ApiResponse } from "../../lib/api/client";
import type { ApiCurrentUser, ApiLoginResponse, LoginPayload } from "../../types";

export async function login(payload: LoginPayload) {
  const response = await apiClient.post<ApiResponse<ApiLoginResponse>>(
    "/auth/login/",
    payload
  );
  return unwrapResponse(response);
}

export async function fetchSession() {
  const response = await apiClient.get<ApiResponse<ApiCurrentUser>>("/auth/me/");
  return unwrapResponse(response);
}
