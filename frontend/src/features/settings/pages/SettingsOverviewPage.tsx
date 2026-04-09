import { PageContainer } from "../../../components/layout/PageContainer";
import { Card } from "../../../components/ui/Card";
import { Link } from "react-router-dom";

const settingsLinks = [
  { label: "Document types", path: "/app/settings/document-types", description: "Define required documents and renewal windows." },
  { label: "Onboarding templates", path: "/app/settings/templates", description: "Configure requirement bundles by vendor type." },
  { label: "Approval flows", path: "/app/settings/approval-flows", description: "Set reviewers, approvers, and escalation paths." },
  { label: "Notification settings", path: "/app/settings/notifications", description: "Manage alerts, reminders, and digests." },
  { label: "Organization profile", path: "/app/settings/organization", description: "Update org details and default settings." },
  { label: "Members & roles", path: "/app/settings/members", description: "Invite and manage team members." },
];

export function SettingsOverviewPage() {
  return (
    <PageContainer
      title="Settings"
      description="Manage organization configuration and compliance workflows."
    >
      <div className="grid gap-4 md:grid-cols-2">
        {settingsLinks.map((item) => (
          <Link key={item.path} to={item.path}>
            <Card className="space-y-2 transition hover:border-blue-200 hover:shadow-soft">
              <p className="text-sm font-semibold text-slate-900">{item.label}</p>
              <p className="text-sm text-slate-600">{item.description}</p>
            </Card>
          </Link>
        ))}
      </div>
    </PageContainer>
  );
}
