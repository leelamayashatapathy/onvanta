# Onvanta Workflow Process + Connections

## Purpose
This document explains how the UI flows connect across onboarding, documents, approvals, expiries, tasks, audit, settings, and members.

## Core Entities
- Organization
- OrganizationMember
- Vendor
- VendorContact
- DocumentType
- OnboardingTemplate
- OnboardingCase
- OnboardingRequirement
- VendorDocument
- ApprovalFlow
- ApprovalStep
- ApprovalDecision
- ActionTask
- AuditEvent

## Primary Navigation
- Dashboard → /app/dashboard
- Vendors → /app/vendors
- Onboarding → /app/onboarding
- Documents → /app/documents
- Approvals → /app/approvals
- Expiries → /app/expiries/upcoming
- Tasks → /app/tasks
- Audit → /app/audit
- Settings → /app/settings

## Workflow Connections

### 1. Vendor Onboarding Intake
- Start at Vendors list: /app/vendors
- Create vendor: /app/vendors/new
- Vendor detail: /app/vendors/:vendorId
- From vendor detail, initiate onboarding case → /app/onboarding/:caseId

Key UI signals
- Vendor status chip + risk indicator
- Vendor code, legal name, category, owner user

### 2. Onboarding Case Execution
- Onboarding list: /app/onboarding
- Case detail: /app/onboarding/:caseId

Key UI signals
- Progress bar and stage
- Checklist items derived from /onboarding/cases/:case_id/checklist/
- Case summary pulled from /onboarding/cases/:case_id/

### 3. Document Collection and Review
- Documents list: /app/documents (requires Vendor ID filter)
- Document detail: /app/documents/:documentId

Key UI signals
- Document status, version, issue/expiry dates
- Upload via /documents/upload/
- Approve/reject via /documents/:document_id/approve/ and /reject/

### 4. Approvals
- Approval queue: /app/approvals
- Approval detail: /app/approvals/:decisionId (decision ID from queue)

Key UI signals
- Decision ID, case ID, step ID
- Approve/reject via /approvals/decisions/:decision_id/approve|reject/
- Case history via /approvals/cases/:case_id/history/

### 5. Expiries and Renewals
- Upcoming expiries: /app/expiries/upcoming → /expiries/upcoming/
- Overdue expiries: /app/expiries/overdue → /expiries/overdue/
- Renewal queue derived from upcoming expiries

### 6. Tasks and Follow-ups
- Task list: /app/tasks → /tasks/
- Task detail: /app/tasks/:taskId → /tasks/:task_id/complete/

### 7. Audit Log
- Global audit: /app/audit → /audit/events/

### 8. Settings and Governance
- Settings overview: /app/settings
- Document types: /app/settings/document-types → /document-types/
- Templates: /app/settings/templates → /onboarding-templates/
- Approval flows: /app/settings/approval-flows → /approvals/flows/
- Organization: /app/settings/organization → /organizations/detail/
- Members: /app/settings/members → /organizations/members/ with role update

## Role-Aware Behavior
- Sidebar items are filtered by role.
- Actions such as settings access are restricted by role; backend is source of truth.

## Data Flow and Integration
- API base URL: http://localhost:8000/api/v1
- Axios client unwraps API responses of shape { message, data, metadata }
- TanStack Query handles server state for lists and detail reads.
- Mock fallback data remains as initial data for offline development.
- Backend CORS configured to allow http://localhost:3000 via `django-cors-headers`.
- Frontend runs on port 3000, backend runs on port 8000.

## Phase 5 Status
- Frontend endpoints aligned with backend routes.
- Auth flow updated to use /auth/login and /auth/me with success_response wrapper.
- Document list now fetches per vendor ID via /vendors/:vendor_id/documents/.
- Approvals now act on decision IDs as required by backend.
- Tasks complete flow matches /tasks/:task_id/complete/.
- Approval flows, templates, and document types use real backend payload shapes.
 - Backend CORS support added for local development on port 3000.
