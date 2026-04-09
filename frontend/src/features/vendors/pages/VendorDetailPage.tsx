import { PageContainer } from "../../../components/layout/PageContainer";
import { PageSection } from "../../../components/layout/PageSection";
import { SectionHeader } from "../../../components/layout/SectionHeader";
import { Card } from "../../../components/ui/Card";
import { Button } from "../../../components/ui/Button";
import { Badge } from "../../../components/ui/Badge";
import { KeyValueList } from "../../../components/ui/KeyValueList";
import { ActivityFeedItem } from "../../../components/workflow/ActivityFeedItem";
import { DocumentCard } from "../../../components/workflow/DocumentCard";
import { RiskIndicator } from "../../../components/workflow/RiskIndicator";
import { useParams } from "react-router-dom";
import { useVendor, useVendorDocuments, useTemplates } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";
import { useStartOnboardingCase } from "../../../lib/api/queries/mutations";
import { Modal } from "../../../components/ui/Modal";
import { useEffect, useState } from "react";
import { Select } from "../../../components/forms/Select";

const activity = [
  {
    title: "Documents approved",
    description: "Insurance COI approved by compliance team.",
    timestamp: "2026-03-18",
  },
  {
    title: "Onboarding submitted",
    description: "Case moved to approval stage by Marcus L.",
    timestamp: "2026-03-12",
  },
];

export function VendorDetailPage() {
  const { vendorId = "" } = useParams();
  const { data: vendor, isLoading, isError } = useVendor(vendorId);
  const { data: documents = [] } = useVendorDocuments(vendorId);
  const { data: templates = [] } = useTemplates();
  const startCaseMutation = useStartOnboardingCase();
  const [open, setOpen] = useState(false);
  const [templateId, setTemplateId] = useState("");

  useEffect(() => {
    if (!templateId && templates.length > 0) {
      setTemplateId(templates[0].id);
    }
  }, [templates, templateId]);

  if (isLoading) {
    return <LoadingState label="Loading vendor profile" />;
  }

  if (isError || !vendor) {
    return (
      <ErrorState
        title="Unable to load vendor"
        description="Please check the vendor ID or try again."
      />
    );
  }

  return (
    <PageContainer
      title={vendor.display_name}
      description="Vendor profile, onboarding readiness, and document health."
      action={
        <Button variant="secondary" onClick={() => setOpen(true)}>
          Start onboarding case
        </Button>
      }
    >
      <PageSection>
        <Card className="space-y-4">
          <SectionHeader>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Vendor status</p>
              <div className="mt-2 flex items-center gap-2">
                <Badge tone={vendor.operational_status === "active" ? "success" : "warning"}>
                  {vendor.operational_status}
                </Badge>
                <RiskIndicator level={vendor.risk_level} />
              </div>
            </div>
            <div className="text-right">
              <p className="text-xs text-slate-500">Vendor code</p>
              <p className="text-sm font-semibold text-slate-900">{vendor.vendor_code}</p>
            </div>
          </SectionHeader>
          <KeyValueList
            items={[
              { label: "Legal name", value: vendor.legal_name },
              { label: "Category", value: vendor.category || "—" },
              { label: "Owner", value: vendor.owner_user ?? "Unassigned" },
              { label: "Onboarding status", value: vendor.onboarding_status },
            ]}
          />
        </Card>
      </PageSection>

      <PageSection className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-4 lg:col-span-2">
          <SectionHeader>
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Documents</h3>
              <p className="text-sm text-slate-600">Latest submissions and review status.</p>
            </div>
          </SectionHeader>
          <div className="grid gap-4">
            {documents.map((doc) => (
              <DocumentCard key={doc.id} document={doc} />
            ))}
          </div>
        </div>

        <div className="space-y-4">
          <SectionHeader>
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Activity</h3>
              <p className="text-sm text-slate-600">Recent updates on this vendor.</p>
            </div>
          </SectionHeader>
          <div className="space-y-3">
            {activity.map((item) => (
              <ActivityFeedItem key={item.title} {...item} />
            ))}
          </div>
        </div>
      </PageSection>

      <Modal title="Start onboarding case" open={open} onClose={() => setOpen(false)}>
        <div className="space-y-4">
          <label className="text-sm font-medium text-slate-700">Select template</label>
          <Select
            value={templateId}
            onChange={(event) => setTemplateId(event.target.value)}
          >
            <option value="">Select template</option>
            {templates.map((tpl) => (
              <option key={tpl.id} value={tpl.id}>
                {tpl.name}
              </option>
            ))}
          </Select>
          <div className="flex justify-end gap-2">
            <Button variant="secondary" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button
              onClick={() => {
                if (!templateId) return;
                startCaseMutation.mutate({ vendor_id: vendor.id, template_id: templateId });
                setOpen(false);
              }}
              disabled={startCaseMutation.isPending || !templateId}
            >
              {startCaseMutation.isPending ? "Starting..." : "Start"}
            </Button>
          </div>
        </div>
      </Modal>
    </PageContainer>
  );
}
