import { PageContainer } from "../../../components/layout/PageContainer";
import { FilterBar } from "../../../components/tables/FilterBar";
import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/forms/Select";
import { AuditEventCard } from "../../../components/workflow/AuditEventCard";
import { useAuditEvents } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";

export function AuditPage() {
  const { data: events = [], isLoading, isError } = useAuditEvents();

  return (
    <PageContainer
      title="Audit log"
      description="Chronological record of compliance and onboarding actions."
    >
      <FilterBar>
        <div className="w-full max-w-xs">
          <Input placeholder="Search audit events" />
        </div>
        <Select className="w-48" defaultValue="">
          <option value="">All entities</option>
          <option value="documents">Documents</option>
          <option value="vendors">Vendors</option>
          <option value="onboarding">Onboarding</option>
        </Select>
      </FilterBar>

      {isLoading ? <LoadingState label="Loading audit events" /> : null}
      {isError ? (
        <ErrorState title="Unable to load audit log" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <div className="grid gap-4 lg:grid-cols-2">
          {events.map((event) => (
            <AuditEventCard key={event.id} event={event} />
          ))}
        </div>
      ) : null}
    </PageContainer>
  );
}
