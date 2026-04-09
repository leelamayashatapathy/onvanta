import { PageContainer } from "../../../components/layout/PageContainer";
import { PageSection } from "../../../components/layout/PageSection";
import { SectionHeader } from "../../../components/layout/SectionHeader";
import { Card } from "../../../components/ui/Card";
import { Button } from "../../../components/ui/Button";
import { ProgressBar } from "../../../components/ui/ProgressBar";
import { ChecklistItem } from "../../../components/workflow/ChecklistItem";
import { ApprovalStepTracker } from "../../../components/workflow/ApprovalStepTracker";
import { KeyValueList } from "../../../components/ui/KeyValueList";
import { useParams } from "react-router-dom";
import { useOnboardingCase, useOnboardingChecklist } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";
import { useSubmitOnboardingCase } from "../../../lib/api/queries/mutations";

function mapRequirementStatus(requirement: { submitted: boolean; verified: boolean }) {
  if (requirement.verified) return "approved";
  if (requirement.submitted) return "submitted";
  return "missing";
}

export function OnboardingDetailPage() {
  const { caseId = "" } = useParams();
  const { data: onboardingCase, isLoading, isError } = useOnboardingCase(caseId);
  const { data: checklist = [] } = useOnboardingChecklist(caseId);
  const submitMutation = useSubmitOnboardingCase();

  if (isLoading) {
    return <LoadingState label="Loading onboarding case" />;
  }

  if (isError || !onboardingCase) {
    return (
      <ErrorState
        title="Unable to load onboarding case"
        description="Please check the case ID or try again."
      />
    );
  }

  return (
    <PageContainer
      title={`Onboarding · ${onboardingCase.id}`}
      description="Track requirements, blockers, and approval readiness."
      action={
        <Button
          onClick={() => submitMutation.mutate(onboardingCase.id)}
          disabled={submitMutation.isPending}
        >
          {submitMutation.isPending ? "Submitting..." : "Submit for review"}
        </Button>
      }
    >
      <PageSection className="grid gap-6 lg:grid-cols-3">
        <Card className="space-y-4 lg:col-span-2">
          <SectionHeader>
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Requirements checklist</h3>
              <p className="text-sm text-slate-600">Monitor required documents and completion.</p>
            </div>
          </SectionHeader>
          <ProgressBar value={onboardingCase.progress_percent} label="Overall progress" tone="warning" />
          <div className="space-y-3">
            {checklist.map((req) => (
              <ChecklistItem
                key={req.id}
                title={`Document ${req.document_type}`}
                status={mapRequirementStatus(req) as "missing" | "submitted" | "approved" | "rejected"}
                owner="Assigned"
                dueDate={req.due_date ?? undefined}
              />
            ))}
          </div>
        </Card>

        <div className="space-y-4">
          <Card className="space-y-4">
            <h3 className="text-lg font-semibold text-slate-900">Case summary</h3>
            <KeyValueList
              items={[
                { label: "Stage", value: onboardingCase.current_stage },
                { label: "Status", value: onboardingCase.status },
                { label: "Vendor", value: onboardingCase.vendor },
                { label: "Template", value: onboardingCase.template },
              ]}
            />
          </Card>
          <Card className="space-y-4">
            <h3 className="text-lg font-semibold text-slate-900">Approval flow</h3>
            <ApprovalStepTracker
              steps={[
                { id: "step-1", label: "Compliance review", status: "approved", actor: "Nina R." },
                { id: "step-2", label: "Security review", status: "pending", actor: "Jordan K." },
                { id: "step-3", label: "Final approval", status: "pending" },
              ]}
            />
          </Card>
        </div>
      </PageSection>
    </PageContainer>
  );
}
