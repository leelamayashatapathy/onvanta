import { PageContainer } from "../../../components/layout/PageContainer";
import { FilterBar } from "../../../components/tables/FilterBar";
import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/forms/Select";
import { ExpiryAlertCard } from "../../../components/workflow/ExpiryAlertCard";
import { useUpcomingExpiries } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";
import { differenceInCalendarDays } from "date-fns";

export function ExpiriesUpcomingPage() {
  const { data: expiries = [], isLoading, isError } = useUpcomingExpiries(30);

  return (
    <PageContainer
      title="Upcoming expiries"
      description="Documents expiring within the next 30 days."
    >
      <FilterBar>
        <div className="w-full max-w-xs">
          <Input placeholder="Search vendors" />
        </div>
        <Select className="w-48" defaultValue="">
          <option value="">All severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </Select>
      </FilterBar>

      {isLoading ? <LoadingState label="Loading expiries" /> : null}
      {isError ? (
        <ErrorState title="Unable to load expiries" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <div className="grid gap-4 md:grid-cols-2">
          {expiries.map((item) => (
            <ExpiryAlertCard
              key={item.document_id}
              vendor={item.vendor_name}
              document={item.document_type}
              daysRemaining={differenceInCalendarDays(new Date(item.expiry_date), new Date())}
              owner={item.vendor_id}
            />
          ))}
        </div>
      ) : null}
    </PageContainer>
  );
}
