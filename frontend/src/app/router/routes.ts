import {
  LayoutGrid,
  Users,
  ClipboardList,
  FileText,
  BadgeCheck,
  Clock3,
  ListChecks,
  ShieldCheck,
  Settings,
} from "lucide-react";
import type { UserRole } from "../../types";

export interface NavItem {
  label: string;
  path: string;
  icon: typeof LayoutGrid;
  roles?: UserRole[];
}

export const NAV_ITEMS: NavItem[] = [
  { label: "Dashboard", path: "/app/dashboard", icon: LayoutGrid },
  {
    label: "Vendors",
    path: "/app/vendors",
    icon: Users,
    roles: ["org_admin", "procurement_manager", "compliance_manager", "read_only"],
  },
  {
    label: "Onboarding",
    path: "/app/onboarding",
    icon: ClipboardList,
    roles: [
      "org_admin",
      "procurement_manager",
      "reviewer",
      "approver",
      "compliance_manager",
      "read_only",
    ],
  },
  {
    label: "Documents",
    path: "/app/documents",
    icon: FileText,
    roles: ["org_admin", "reviewer", "compliance_manager", "read_only"],
  },
  {
    label: "Approvals",
    path: "/app/approvals",
    icon: BadgeCheck,
    roles: ["org_admin", "approver", "reviewer", "compliance_manager"],
  },
  {
    label: "Expiries",
    path: "/app/expiries/upcoming",
    icon: Clock3,
    roles: ["org_admin", "compliance_manager", "read_only"],
  },
  {
    label: "Tasks",
    path: "/app/tasks",
    icon: ListChecks,
    roles: [
      "org_admin",
      "procurement_manager",
      "reviewer",
      "approver",
      "compliance_manager",
    ],
  },
  {
    label: "Audit",
    path: "/app/audit",
    icon: ShieldCheck,
    roles: ["org_admin", "compliance_manager", "read_only"],
  },
  {
    label: "Settings",
    path: "/app/settings",
    icon: Settings,
    roles: ["org_admin"],
  },
];

export const ROUTE_TITLES: Record<string, string> = {
  "/app/dashboard": "Executive Overview",
  "/app/vendors": "Vendors",
  "/app/vendors/new": "Create Vendor",
  "/app/onboarding": "Onboarding Cases",
  "/app/documents": "Documents",
  "/app/approvals": "Approval Queue",
  "/app/expiries/upcoming": "Upcoming Expiries",
  "/app/expiries/overdue": "Overdue Expiries",
  "/app/expiries/renewals": "Renewal Queue",
  "/app/tasks": "Tasks",
  "/app/audit": "Audit Log",
  "/app/settings": "Settings",
  "/app/settings/document-types": "Document Types",
  "/app/settings/templates": "Onboarding Templates",
  "/app/settings/approval-flows": "Approval Flows",
  "/app/settings/notifications": "Notification Settings",
  "/app/settings/organization": "Organization Profile",
  "/app/settings/members": "Members & Roles",
};
