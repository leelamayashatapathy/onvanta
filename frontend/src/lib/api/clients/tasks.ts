import { apiClient, unwrapResponse, type ApiResponse } from "../client";
import type { ActionTask } from "../../../types";

export async function fetchTasks() {
  const response = await apiClient.get<ApiResponse<ActionTask[]>>("/tasks/");
  return unwrapResponse(response);
}

export async function completeTask(taskId: string) {
  const response = await apiClient.post<ApiResponse<ActionTask>>(`/tasks/${taskId}/complete/`);
  return unwrapResponse(response);
}
