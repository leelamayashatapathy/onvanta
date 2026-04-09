import { PageContainer } from "../../../components/layout/PageContainer";
import { FilterBar } from "../../../components/tables/FilterBar";
import { DataTable } from "../../../components/tables/DataTable";
import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/forms/Select";
import { Badge } from "../../../components/ui/Badge";
import { Link } from "react-router-dom";
import { useApprovals } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";

export function ApprovalsPage() {
  const { data: approvals = [], isLoading, isError } = useApprovals();

  return (
    <PageContainer
      title="Approval queue"
      description="Decisions required from approvers and compliance leads."
    >
      <FilterBar>
        <div className="w-full max-w-xs">
          <Input placeholder="Search approvals" />
        </div>
        <Select className="w-48" defaultValue="">
          <option value="">All statuses</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </Select>
      </FilterBar>

      {isLoading ? <LoadingState label="Loading approvals" /> : null}
      {isError ? (
        <ErrorState title="Unable to load approvals" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <DataTable
          columns={["Decision", "Case", "Step", "Status", "Action"]}
          rows={approvals.map((item) => [
            <div key={item.id}>
              <p className="text-sm font-semibold text-slate-900">Decision {item.id}</p>
            </div>,
            <span key={`${item.id}-case`} className="text-sm text-slate-600">
              {item.onboarding_case}
            </span>,
            <span key={`${item.id}-step`} className="text-sm text-slate-600">
              {item.approval_step}
            </span>,
            <Badge
              key={`${item.id}-status`}
              tone={item.decision === "approved" ? "success" : item.decision === "rejected" ? "error" : "warning"}
            >
              {item.decision}
            </Badge>,
            <Link key={`${item.id}-action`} to={`/app/approvals/${item.id}`} className="text-sm font-medium text-blue-600">
              Review
            </Link>,
          ])}
        />
      ) : null}
    </PageContainer>
  );
}
