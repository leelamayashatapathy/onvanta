import axios, { AxiosError, type AxiosInstance, type AxiosResponse } from "axios";
import { tokenStorage } from "./tokens";
import type { AuthTokens } from "../../types";

export interface ApiResponse<T> {
  message: string;
  data: T;
  metadata?: Record<string, unknown>;
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

let isRefreshing = false;
let refreshQueue: Array<(tokens: AuthTokens | null) => void> = [];

const resolveQueue = (tokens: AuthTokens | null) => {
  refreshQueue.forEach((callback) => callback(tokens));
  refreshQueue = [];
};

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: false,
});

apiClient.interceptors.request.use((config) => {
  const tokens = tokenStorage.getTokens();
  if (tokens?.access) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${tokens.access}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config;
    if (!originalRequest) {
      return Promise.reject(error);
    }

    const status = error.response?.status;
    if (status !== 401) {
      return Promise.reject(error);
    }

    if (originalRequest.url?.includes("/auth/refresh")) {
      tokenStorage.clearAll();
      return Promise.reject(error);
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        refreshQueue.push((tokens) => {
          if (!tokens?.access) {
            reject(error);
            return;
          }
          originalRequest.headers = originalRequest.headers ?? {};
          originalRequest.headers.Authorization = `Bearer ${tokens.access}`;
          resolve(apiClient(originalRequest));
        });
      });
    }

    isRefreshing = true;

    try {
      const refreshed = await refreshToken();
      if (!refreshed) {
        resolveQueue(null);
        return Promise.reject(error);
      }
      resolveQueue(refreshed);
      originalRequest.headers = originalRequest.headers ?? {};
      originalRequest.headers.Authorization = `Bearer ${refreshed.access}`;
      return apiClient(originalRequest);
    } catch (refreshError) {
      resolveQueue(null);
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export function unwrapResponse<T>(response: AxiosResponse<ApiResponse<T>>) {
  return response.data.data;
}

export async function refreshToken(): Promise<AuthTokens | null> {
  const tokens = tokenStorage.getTokens();
  if (!tokens?.refresh) return null;

  const response = await axios.post<ApiResponse<{ access: string }>>(
    `${API_BASE_URL}/auth/refresh/`,
    { refresh: tokens.refresh },
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  const access = response.data.data.access;
  tokenStorage.setAccessToken(access);
  return { ...tokens, access };
}
