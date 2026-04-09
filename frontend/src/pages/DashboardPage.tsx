import { Badge } from "../components/ui/Badge";
import { PageContainer } from "../components/layout/PageContainer";
import { Button } from "../components/ui/Button";
import { MetricCard } from "../components/ui/MetricCard";
import { Card } from "../components/ui/Card";
import { useDashboardSummary, useApprovals, useUpcomingExpiries } from "../lib/api/queries/hooks";
import { LoadingState } from "../components/feedback/LoadingState";

export function DashboardPage() {
  const { data: summary, isLoading } = useDashboardSummary();
  const { data: approvals = [] } = useApprovals();
  const { data: expiries = [] } = useUpcomingExpiries(30);

  if (isLoading || !summary) {
    return <LoadingState label="Loading dashboard" />;
  }

  return (
    <PageContainer
      title="Executive Overview"
      description="Operational signals across onboarding, approvals, and compliance."
      action={<Button>New vendor</Button>}
    >
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          label="Total vendors"
          value={`${summary.organization.vendors_total}`}
          helper={`${summary.organization.vendors_active} active`}
        />
        <MetricCard
          label="Onboarding active"
          value={`${summary.organization.onboarding_active}`}
          helper="Cases in progress"
        />
        <MetricCard
          label="Approvals pending"
          value={`${summary.pending_approvals.pending_approvals}`}
          helper="Awaiting decisions"
        />
        <MetricCard
          label="Expiring (30d)"
          value={`${summary.expiries.upcoming}`}
          helper={`${summary.expiries.overdue} overdue`}
        />
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <Card className="space-y-4 lg:col-span-2">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Pending approvals</h3>
              <p className="text-sm text-slate-600">Decisions required from your team.</p>
            </div>
            <Button variant="secondary" size="sm">
              View queue
            </Button>
          </div>
          <div className="space-y-3">
            {approvals.slice(0, 3).map((item) => (
              <div
                key={item.id}
                className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
              >
                <div>
                  <p className="text-sm font-semibold text-slate-900">Case {item.onboarding_case}</p>
                  <p className="text-xs text-slate-500">Step {item.approval_step}</p>
                </div>
                <div className="flex items-center gap-3">
                  <Badge tone="warning">{item.decision}</Badge>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold text-slate-900">Expiring soon</h3>
            <p className="text-sm text-slate-600">Documents expiring within 30 days.</p>
          </div>
          <div className="space-y-3">
            {expiries.slice(0, 2).map((item) => (
              <div key={item.document_id} className="rounded-xl border border-slate-200 px-4 py-3">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-semibold text-slate-900">{item.vendor_name}</p>
                  <Badge tone="warning">{item.expiry_date}</Badge>
                </div>
                <p className="text-xs text-slate-500">{item.document_type}</p>
              </div>
            ))}
          </div>
          <Button variant="secondary" size="sm">
            Review expiries
          </Button>
        </Card>
      </section>
    </PageContainer>
  );
}
