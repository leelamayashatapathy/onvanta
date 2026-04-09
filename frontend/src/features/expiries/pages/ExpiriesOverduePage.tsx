import { PageContainer } from "../../../components/layout/PageContainer";
import { ExpiryAlertCard } from "../../../components/workflow/ExpiryAlertCard";
import { useOverdueExpiries } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";
import { differenceInCalendarDays } from "date-fns";

export function ExpiriesOverduePage() {
  const { data: expiries = [], isLoading, isError } = useOverdueExpiries();

  return (
    <PageContainer
      title="Overdue expiries"
      description="Documents that are past expiry and require immediate action."
    >
      {isLoading ? <LoadingState label="Loading overdue expiries" /> : null}
      {isError ? (
        <ErrorState title="Unable to load overdue" description="Please retry once the backend is available." />
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
