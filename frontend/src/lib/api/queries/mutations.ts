import { useMutation, useQueryClient } from "@tanstack/react-query";
import { QUERY_KEYS } from "./keys";
import {
  createVendor,
  type CreateVendorPayload,
} from "../clients/vendors";
import {
  submitOnboardingCase,
  startOnboardingCase,
} from "../clients/onboarding";
import {
  uploadDocument,
  approveDocument,
  rejectDocument,
  type UploadDocumentPayload,
} from "../clients/documents";
import { approveDecision, rejectDecision, createApprovalFlow } from "../clients/approvals";
import { completeTask } from "../clients/tasks";
import {
  createDocumentType,
  createTemplate,
  type CreateDocumentTypePayload,
  type CreateTemplatePayload,
} from "../clients/settings";
import { updateMemberRole } from "../clients/members";

export function useCreateVendor() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateVendorPayload) => createVendor(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.vendors });
    },
  });
}

export function useStartOnboardingCase() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: { vendor_id: string; template_id: string }) => startOnboardingCase(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.onboarding });
    },
  });
}

export function useSubmitOnboardingCase() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (caseId: string) => submitOnboardingCase(caseId),
    onSuccess: (_, caseId) => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.onboarding });
      queryClient.invalidateQueries({ queryKey: [...QUERY_KEYS.onboarding, caseId] });
    },
  });
}

export function useUploadDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: UploadDocumentPayload) => uploadDocument(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.documents });
    },
  });
}

export function useApproveDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (documentId: string) => approveDocument(documentId),
    onSuccess: (_, documentId) => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.documents });
      queryClient.invalidateQueries({ queryKey: [...QUERY_KEYS.documents, documentId] });
    },
  });
}

export function useRejectDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ documentId, rejection_reason }: { documentId: string; rejection_reason: string }) =>
      rejectDocument(documentId, rejection_reason),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.documents });
      queryClient.invalidateQueries({ queryKey: [...QUERY_KEYS.documents, variables.documentId] });
    },
  });
}

export function useApproveDecision() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ decisionId, comments }: { decisionId: string; comments?: string }) =>
      approveDecision(decisionId, comments),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.approvals });
    },
  });
}

export function useRejectDecision() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ decisionId, comments }: { decisionId: string; comments?: string }) =>
      rejectDecision(decisionId, comments),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.approvals });
    },
  });
}

export function useCreateApprovalFlow() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: { name: string; scope: string; active: boolean }) => createApprovalFlow(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [...QUERY_KEYS.approvals, "flows"] });
    },
  });
}

export function useCompleteTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (taskId: string) => completeTask(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.tasks });
    },
  });
}

export function useCreateDocumentType() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateDocumentTypePayload) => createDocumentType(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [...QUERY_KEYS.settings, "document-types"] });
    },
  });
}

export function useCreateTemplate() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateTemplatePayload) => createTemplate(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [...QUERY_KEYS.settings, "templates"] });
    },
  });
}

export function useUpdateMemberRole() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ memberId, role }: { memberId: string; role: "org_admin" | "procurement_manager" | "reviewer" | "approver" | "compliance_manager" | "read_only" }) =>
      updateMemberRole(memberId, role),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.members });
    },
  });
}
