import type {
  Vendor,
  VendorDocument,
  OnboardingCase,
  ApprovalDecision,
  ApprovalFlow,
  ActionTask,
  AuditEvent,
  DocumentType,
  OnboardingTemplate,
  OrganizationMember,
  ExpiryItem,
  OrganizationDetail,
} from "../../types";
import type { DashboardSummary } from "../api/clients/dashboard";

export const mockVendors: Vendor[] = [
  {
    id: "11111111-1111-1111-1111-111111111111",
    vendor_code: "VEN-001",
    legal_name: "Northwind Logistics LLC",
    display_name: "Northwind Logistics",
    vendor_type: "Logistics",
    category: "Logistics",
    risk_level: "high",
    owner_user: null,
    onboarding_status: "under_review",
    operational_status: "active",
    notes: "Priority logistics provider",
    created_at: "2026-02-18",
    updated_at: "2026-03-01",
  },
];

export const mockDocuments: VendorDocument[] = [
  {
    id: "22222222-2222-2222-2222-222222222222",
    vendor: "11111111-1111-1111-1111-111111111111",
    document_type: "33333333-3333-3333-3333-333333333333",
    file: "",
    file_path: "",
    original_name: "Insurance COI.pdf",
    mime_type: "application/pdf",
    file_size: 123456,
    checksum: "checksum",
    version: 1,
    issue_date: "2025-11-10",
    expiry_date: "2026-11-10",
    status: "active",
    verification_status: "approved",
    verified_by: null,
    verified_at: null,
    rejection_reason: null,
    supersedes_document: null,
    uploaded_by: null,
    uploaded_at: "2026-01-02",
    created_at: "2026-01-02",
    updated_at: "2026-01-02",
  },
];

export const mockOnboardingCases: OnboardingCase[] = [
  {
    id: "44444444-4444-4444-4444-444444444444",
    vendor: "11111111-1111-1111-1111-111111111111",
    template: "55555555-5555-5555-5555-555555555555",
    current_stage: "approval",
    status: "approval_pending",
    progress_percent: 82,
    started_at: "2026-03-01",
    submitted_at: "2026-03-10",
    completed_at: null,
    blocked_reason: null,
    created_at: "2026-03-01",
    updated_at: "2026-03-10",
  },
];

export const mockApprovals: ApprovalDecision[] = [
  {
    id: "66666666-6666-6666-6666-666666666666",
    onboarding_case: "44444444-4444-4444-4444-444444444444",
    approval_step: "77777777-7777-7777-7777-777777777777",
    decision: "pending",
    decided_by: null,
    decided_at: null,
    comments: "",
    created_at: "2026-03-11",
    updated_at: "2026-03-11",
  },
];

export const mockApprovalFlows: ApprovalFlow[] = [
  {
    id: "flow-1",
    name: "Standard approval",
    scope: "default",
    active: true,
    created_at: "2026-02-01",
    updated_at: "2026-02-01",
  },
];

export const mockTasks: ActionTask[] = [
  {
    id: "88888888-8888-8888-8888-888888888888",
    organization: "99999999-9999-9999-9999-999999999999",
    vendor: "11111111-1111-1111-1111-111111111111",
    onboarding_case: "44444444-4444-4444-4444-444444444444",
    task_type: "review",
    title: "Review insurance renewal",
    description: "Verify renewal documents",
    assigned_to: null,
    due_date: "2026-04-10",
    status: "open",
    priority: "high",
    created_at: "2026-04-01",
    updated_at: "2026-04-01",
  },
];

export const mockAuditEvents: AuditEvent[] = [
  {
    id: "aud-1",
    organization: "99999999-9999-9999-9999-999999999999",
    actor_user: "user-1",
    actor_type: "user",
    entity_type: "vendor_document",
    entity_id: "22222222-2222-2222-2222-222222222222",
    action: "document_approved",
    source: "system",
    old_data_json: null,
    new_data_json: null,
    created_at: "2026-04-08",
  },
];

export const mockDocumentTypes: DocumentType[] = [
  {
    id: "33333333-3333-3333-3333-333333333333",
    code: "COI",
    name: "Insurance COI",
    description: "Certificate of insurance",
    category: "Insurance",
    is_mandatory: true,
    has_expiry: true,
    expiry_warning_days: 30,
    criticality: "high",
    applies_to_vendor_type: "",
    allowed_extensions: ["pdf"],
    max_file_size_mb: 10,
  },
];

export const mockTemplates: OnboardingTemplate[] = [
  {
    id: "55555555-5555-5555-5555-555555555555",
    name: "Standard vendor",
    applies_to_vendor_category: "General",
    active: true,
    created_at: "2026-01-01",
    updated_at: "2026-01-01",
  },
];

export const mockMembers: OrganizationMember[] = [
  {
    id: "mem-1",
    user_id: "user-1",
    email: "marcus@onvanta.com",
    role: "procurement_manager",
    status: "active",
  },
];

export const mockOrganization: OrganizationDetail = {
  id: "99999999-9999-9999-9999-999999999999",
  name: "Onvanta Holdings",
  slug: "onvanta",
  industry: "SaaS",
  size: "51-200",
  timezone: "UTC",
  settings_json: {},
};

export const mockExpiries: ExpiryItem[] = [
  {
    document_id: "22222222-2222-2222-2222-222222222222",
    vendor_id: "11111111-1111-1111-1111-111111111111",
    vendor_name: "Northwind Logistics",
    document_type: "Insurance COI",
    expiry_date: "2026-11-10",
  },
];

export const mockDashboard: DashboardSummary = {
  organization: {
    vendors_total: 1,
    vendors_active: 1,
    onboarding_active: 1,
  },
  pending_approvals: {
    pending_approvals: 1,
  },
  pipeline: {
    approval_pending: 1,
  },
  expiries: {
    upcoming: 1,
    overdue: 0,
  },
};
