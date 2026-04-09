import { PageContainer } from "../../../components/layout/PageContainer";
import { FilterBar } from "../../../components/tables/FilterBar";
import { DataTable } from "../../../components/tables/DataTable";
import { Button } from "../../../components/ui/Button";
import { Badge } from "../../../components/ui/Badge";
import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/forms/Select";
import { RiskIndicator } from "../../../components/workflow/RiskIndicator";
import { Link } from "react-router-dom";
import { useVendors } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";

export function VendorListPage() {
  const { data: vendors = [], isLoading, isError } = useVendors();

  return (
    <PageContainer
      title="Vendors"
      description="Track vendor status, risk, and onboarding readiness."
      action={
        <Link to="/app/vendors/new">
          <Button>New vendor</Button>
        </Link>
      }
    >
      <FilterBar>
        <div className="w-full max-w-xs">
          <Input placeholder="Search vendors" />
        </div>
        <Select className="w-48" defaultValue="">
          <option value="">All statuses</option>
          <option value="active">Active</option>
          <option value="pending">Pending</option>
          <option value="blocked">Blocked</option>
        </Select>
      </FilterBar>

      {isLoading ? <LoadingState label="Loading vendors" /> : null}
      {isError ? (
        <ErrorState title="Unable to load vendors" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <DataTable
          columns={["Vendor", "Status", "Risk", "Owner", "Category", "Actions"]}
          rows={vendors.map((vendor) => [
            <div key={vendor.id}>
              <p className="text-sm font-semibold text-slate-900">{vendor.display_name}</p>
              <p className="text-xs text-slate-500">{vendor.vendor_code}</p>
            </div>,
            <Badge
              key={`${vendor.id}-status`}
              tone={vendor.operational_status === "active" ? "success" : "warning"}
            >
              {vendor.operational_status}
            </Badge>,
            <RiskIndicator key={`${vendor.id}-risk`} level={vendor.risk_level} />,
            <span key={`${vendor.id}-owner`} className="text-sm text-slate-600">
              {vendor.owner_user ?? "Unassigned"}
            </span>,
            <span key={`${vendor.id}-category`} className="text-sm text-slate-600">
              {vendor.category || "—"}
            </span>,
            <Link key={`${vendor.id}-action`} to={`/app/vendors/${vendor.id}`} className="text-sm font-medium text-blue-600">
              View profile
            </Link>,
          ])}
        />
      ) : null}
    </PageContainer>
  );
}
