import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthLayout } from "../../features/auth/components/AuthLayout";
import { LoginPage } from "../../features/auth/pages/LoginPage";
import { ForgotPasswordPage } from "../../features/auth/pages/ForgotPasswordPage";
import { AppShell } from "../../components/layout/AppShell";
import { ProtectedRoute } from "./ProtectedRoute";
import { DashboardPage } from "../../pages/DashboardPage";
import { VendorListPage } from "../../features/vendors/pages/VendorListPage";
import { VendorDetailPage } from "../../features/vendors/pages/VendorDetailPage";
import { VendorCreatePage } from "../../features/vendors/pages/VendorCreatePage";
import { OnboardingListPage } from "../../features/onboarding/pages/OnboardingListPage";
import { OnboardingDetailPage } from "../../features/onboarding/pages/OnboardingDetailPage";
import { DocumentListPage } from "../../features/documents/pages/DocumentListPage";
import { DocumentDetailPage } from "../../features/documents/pages/DocumentDetailPage";
import { ApprovalsPage } from "../../features/approvals/pages/ApprovalsPage";
import { ApprovalDetailPage } from "../../features/approvals/pages/ApprovalDetailPage";
import { ExpiriesUpcomingPage } from "../../features/expiries/pages/ExpiriesUpcomingPage";
import { ExpiriesOverduePage } from "../../features/expiries/pages/ExpiriesOverduePage";
import { ExpiriesRenewalsPage } from "../../features/expiries/pages/ExpiriesRenewalsPage";
import { TasksPage } from "../../features/tasks/pages/TasksPage";
import { TaskDetailPage } from "../../features/tasks/pages/TaskDetailPage";
import { AuditPage } from "../../features/audit/pages/AuditPage";
import { SettingsOverviewPage } from "../../features/settings/pages/SettingsOverviewPage";
import { DocumentTypesPage } from "../../features/settings/pages/DocumentTypesPage";
import { TemplatesPage } from "../../features/settings/pages/TemplatesPage";
import { ApprovalFlowsPage } from "../../features/settings/pages/ApprovalFlowsPage";
import { NotificationSettingsPage } from "../../features/settings/pages/NotificationSettingsPage";
import { OrganizationSettingsPage } from "../../features/settings/pages/OrganizationSettingsPage";
import { MembersPage } from "../../features/members/pages/MembersPage";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        </Route>

        <Route element={<ProtectedRoute />}>
          <Route element={<AppShell />}>
            <Route path="/app/dashboard" element={<DashboardPage />} />
            <Route path="/app/vendors" element={<VendorListPage />} />
            <Route path="/app/vendors/new" element={<VendorCreatePage />} />
            <Route path="/app/vendors/:vendorId" element={<VendorDetailPage />} />
            <Route path="/app/onboarding" element={<OnboardingListPage />} />
            <Route path="/app/onboarding/:caseId" element={<OnboardingDetailPage />} />
            <Route path="/app/documents" element={<DocumentListPage />} />
            <Route path="/app/documents/:documentId" element={<DocumentDetailPage />} />
            <Route path="/app/approvals" element={<ApprovalsPage />} />
            <Route path="/app/approvals/:decisionId" element={<ApprovalDetailPage />} />
            <Route path="/app/expiries/upcoming" element={<ExpiriesUpcomingPage />} />
            <Route path="/app/expiries/overdue" element={<ExpiriesOverduePage />} />
            <Route path="/app/expiries/renewals" element={<ExpiriesRenewalsPage />} />
            <Route path="/app/tasks" element={<TasksPage />} />
            <Route path="/app/tasks/:taskId" element={<TaskDetailPage />} />
            <Route path="/app/audit" element={<AuditPage />} />
            <Route path="/app/settings" element={<SettingsOverviewPage />} />
            <Route path="/app/settings/document-types" element={<DocumentTypesPage />} />
            <Route path="/app/settings/templates" element={<TemplatesPage />} />
            <Route path="/app/settings/approval-flows" element={<ApprovalFlowsPage />} />
            <Route path="/app/settings/notifications" element={<NotificationSettingsPage />} />
            <Route path="/app/settings/organization" element={<OrganizationSettingsPage />} />
            <Route path="/app/settings/members" element={<MembersPage />} />
            <Route path="/app" element={<Navigate to="/app/dashboard" replace />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
