import { PageContainer } from "../../../components/layout/PageContainer";
import { FilterBar } from "../../../components/tables/FilterBar";
import { DataTable } from "../../../components/tables/DataTable";
import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/forms/Select";
import { Badge } from "../../../components/ui/Badge";
import { Link } from "react-router-dom";
import { useOnboardingCases } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";

export function OnboardingListPage() {
  const { data: cases = [], isLoading, isError } = useOnboardingCases();

  return (
    <PageContainer
      title="Onboarding"
      description="Monitor cases, blockers, and readiness for approval."
    >
      <FilterBar>
        <div className="w-full max-w-xs">
          <Input placeholder="Search cases" />
        </div>
        <Select className="w-48" defaultValue="">
          <option value="">All stages</option>
          <option value="intake">Intake</option>
          <option value="requirements">Requirements</option>
          <option value="review">Review</option>
          <option value="approval">Approval</option>
        </Select>
      </FilterBar>

      {isLoading ? <LoadingState label="Loading onboarding cases" /> : null}
      {isError ? (
        <ErrorState title="Unable to load cases" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <DataTable
          columns={["Case", "Stage", "Status", "Progress", "Action"]}
          rows={cases.map((item) => [
            <div key={item.id}>
              <p className="text-sm font-semibold text-slate-900">Case {item.id}</p>
              <p className="text-xs text-slate-500">Vendor {item.vendor}</p>
            </div>,
            <Badge key={`${item.id}-stage`} tone="info">
              {item.current_stage}
            </Badge>,
            <span key={`${item.id}-status`} className="text-sm text-slate-600">
              {item.status}
            </span>,
            <span key={`${item.id}-progress`} className="text-sm text-slate-600">
              {item.progress_percent}%
            </span>,
            <Link
              key={`${item.id}-action`}
              to={`/app/onboarding/${item.id}`}
              className="text-sm font-medium text-blue-600"
            >
              View case
            </Link>,
          ])}
        />
      ) : null}
    </PageContainer>
  );
}
