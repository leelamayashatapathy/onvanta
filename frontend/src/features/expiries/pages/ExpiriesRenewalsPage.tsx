import { PageContainer } from "../../../components/layout/PageContainer";
import { DataTable } from "../../../components/tables/DataTable";
import { Badge } from "../../../components/ui/Badge";
import { useUpcomingExpiries } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";

export function ExpiriesRenewalsPage() {
  const { data: expiries = [], isLoading, isError } = useUpcomingExpiries(60);

  const renewals = expiries.map((item) => ({
    vendor: item.vendor_name,
    document: item.document_type,
    due: item.expiry_date,
    owner: item.vendor_id,
    status: "Pending upload",
  }));

  return (
    <PageContainer
      title="Renewal queue"
      description="Track renewals and submissions in progress."
    >
      {isLoading ? <LoadingState label="Loading renewals" /> : null}
      {isError ? (
        <ErrorState title="Unable to load renewals" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <DataTable
          columns={["Vendor", "Document", "Due", "Owner", "Status"]}
          rows={renewals.map((item) => [
            <span key={`${item.vendor}-name`} className="text-sm font-semibold text-slate-900">
              {item.vendor}
            </span>,
            <span key={`${item.vendor}-doc`} className="text-sm text-slate-600">
              {item.document}
            </span>,
            <span key={`${item.vendor}-due`} className="text-sm text-slate-600">
              {item.due}
            </span>,
            <span key={`${item.vendor}-owner`} className="text-sm text-slate-600">
              {item.owner}
            </span>,
            <Badge key={`${item.vendor}-status`} tone="warning">
              {item.status}
            </Badge>,
          ])}
        />
      ) : null}
    </PageContainer>
  );
}
