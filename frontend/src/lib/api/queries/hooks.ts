import { useQuery } from "@tanstack/react-query";
import { QUERY_KEYS } from "./keys";
import { fetchVendors, fetchVendorById } from "../clients/vendors";
import { fetchOnboardingCase, fetchOnboardingCases, fetchOnboardingChecklist } from "../clients/onboarding";
import { fetchVendorDocuments, fetchDocument } from "../clients/documents";
import { fetchApprovals, fetchApprovalHistory, fetchApprovalFlows } from "../clients/approvals";
import { fetchUpcomingExpiries, fetchOverdueExpiries } from "../clients/expiries";
import { fetchTasks } from "../clients/tasks";
import { fetchAuditEvents } from "../clients/audit";
import { fetchDocumentTypes, fetchTemplates } from "../clients/settings";
import { fetchMembers } from "../clients/members";
import { fetchDashboardSummary } from "../clients/dashboard";
import { fetchOrganizationDetail } from "../clients/organizations";
import {
  mockVendors,
  mockOnboardingCases,
  mockDocuments,
  mockApprovals,
  mockApprovalFlows,
  mockTasks,
  mockAuditEvents,
  mockDocumentTypes,
  mockTemplates,
  mockMembers,
  mockExpiries,
  mockDashboard,
  mockOrganization,
} from "../../constants/mockData";

export function useDashboardSummary() {
  return useQuery({
    queryKey: QUERY_KEYS.dashboard,
    queryFn: fetchDashboardSummary,
    initialData: mockDashboard,
  });
}

export function useOrganizationDetail() {
  return useQuery({
    queryKey: [...QUERY_KEYS.settings, "organization"],
    queryFn: fetchOrganizationDetail,
    initialData: mockOrganization,
  });
}

export function useVendors() {
  return useQuery({
    queryKey: QUERY_KEYS.vendors,
    queryFn: fetchVendors,
    initialData: mockVendors,
  });
}

export function useVendor(vendorId: string) {
  return useQuery({
    queryKey: QUERY_KEYS.vendor(vendorId),
    queryFn: () => fetchVendorById(vendorId),
    initialData: mockVendors.find((vendor) => vendor.id === vendorId),
    enabled: Boolean(vendorId),
  });
}

export function useOnboardingCases() {
  return useQuery({
    queryKey: QUERY_KEYS.onboarding,
    queryFn: fetchOnboardingCases,
    initialData: mockOnboardingCases,
  });
}

export function useOnboardingCase(caseId: string) {
  return useQuery({
    queryKey: [...QUERY_KEYS.onboarding, caseId],
    queryFn: () => fetchOnboardingCase(caseId),
    initialData: mockOnboardingCases.find((item) => item.id === caseId),
    enabled: Boolean(caseId),
  });
}

export function useOnboardingChecklist(caseId: string) {
  return useQuery({
    queryKey: [...QUERY_KEYS.onboarding, caseId, "checklist"],
    queryFn: () => fetchOnboardingChecklist(caseId),
    enabled: Boolean(caseId),
  });
}

export function useVendorDocuments(vendorId: string) {
  return useQuery({
    queryKey: [...QUERY_KEYS.documents, vendorId],
    queryFn: () => fetchVendorDocuments(vendorId),
    initialData: mockDocuments.filter((doc) => doc.vendor === vendorId),
    enabled: Boolean(vendorId),
  });
}

export function useDocument(documentId: string) {
  return useQuery({
    queryKey: [...QUERY_KEYS.documents, documentId],
    queryFn: () => fetchDocument(documentId),
    initialData: mockDocuments.find((doc) => doc.id === documentId),
    enabled: Boolean(documentId),
  });
}

export function useApprovals() {
  return useQuery({
    queryKey: QUERY_KEYS.approvals,
    queryFn: fetchApprovals,
    initialData: mockApprovals,
  });
}

export function useApprovalHistory(caseId: string) {
  return useQuery({
    queryKey: [...QUERY_KEYS.approvals, caseId, "history"],
    queryFn: () => fetchApprovalHistory(caseId),
    enabled: Boolean(caseId),
  });
}

export function useApprovalFlows() {
  return useQuery({
    queryKey: [...QUERY_KEYS.approvals, "flows"],
    queryFn: fetchApprovalFlows,
    initialData: mockApprovalFlows,
  });
}

export function useUpcomingExpiries(days = 30) {
  return useQuery({
    queryKey: [...QUERY_KEYS.expiries, "upcoming", days],
    queryFn: () => fetchUpcomingExpiries(days),
    initialData: mockExpiries,
  });
}

export function useOverdueExpiries() {
  return useQuery({
    queryKey: [...QUERY_KEYS.expiries, "overdue"],
    queryFn: fetchOverdueExpiries,
    initialData: mockExpiries,
  });
}

export function useTasks() {
  return useQuery({
    queryKey: QUERY_KEYS.tasks,
    queryFn: fetchTasks,
    initialData: mockTasks,
  });
}

export function useAuditEvents() {
  return useQuery({
    queryKey: QUERY_KEYS.audit,
    queryFn: fetchAuditEvents,
    initialData: mockAuditEvents,
  });
}

export function useDocumentTypes() {
  return useQuery({
    queryKey: [...QUERY_KEYS.settings, "document-types"],
    queryFn: fetchDocumentTypes,
    initialData: mockDocumentTypes,
  });
}

export function useTemplates() {
  return useQuery({
    queryKey: [...QUERY_KEYS.settings, "templates"],
    queryFn: fetchTemplates,
    initialData: mockTemplates,
  });
}

export function useMembers() {
  return useQuery({
    queryKey: QUERY_KEYS.members,
    queryFn: fetchMembers,
    initialData: mockMembers,
  });
}
