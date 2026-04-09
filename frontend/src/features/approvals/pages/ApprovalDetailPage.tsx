import { PageContainer } from "../../../components/layout/PageContainer";
import { PageSection } from "../../../components/layout/PageSection";
import { SectionHeader } from "../../../components/layout/SectionHeader";
import { Card } from "../../../components/ui/Card";
import { Button } from "../../../components/ui/Button";
import { ApprovalStepTracker } from "../../../components/workflow/ApprovalStepTracker";
import { KeyValueList } from "../../../components/ui/KeyValueList";
import { Modal } from "../../../components/ui/Modal";
import { useState } from "react";
import { useApproveDecision, useRejectDecision } from "../../../lib/api/queries/mutations";
import { useParams } from "react-router-dom";
import { useApprovals, useApprovalHistory } from "../../../lib/api/queries/hooks";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { FormField } from "../../../components/forms/FormField";
import { Textarea } from "../../../components/forms/Textarea";
import { LoadingState } from "../../../components/feedback/LoadingState";

const rejectSchema = z.object({
  comments: z.string().min(4, "Reason is required"),
});

type RejectFormValues = z.infer<typeof rejectSchema>;

export function ApprovalDetailPage() {
  const { decisionId = "" } = useParams();
  const [rejectOpen, setRejectOpen] = useState(false);
  const approveMutation = useApproveDecision();
  const rejectMutation = useRejectDecision();
  const { data: approvals = [] } = useApprovals();
  const decision = approvals.find((item) => item.id === decisionId);
  const { data: history = [], isLoading: historyLoading } = useApprovalHistory(
    decision?.onboarding_case ?? ""
  );

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RejectFormValues>({
    resolver: zodResolver(rejectSchema),
  });

  const onReject = async (values: RejectFormValues) => {
    await rejectMutation.mutateAsync({ decisionId, comments: values.comments });
    setRejectOpen(false);
  };

  if (!decision) {
    return <LoadingState label="Loading decision" />;
  }

  return (
    <PageContainer
      title="Approval review"
      description="Review onboarding case readiness and decision history."
      action={
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => setRejectOpen(true)}>
            Reject
          </Button>
          <Button
            onClick={() => approveMutation.mutate({ decisionId })}
            disabled={approveMutation.isPending}
          >
            {approveMutation.isPending ? "Approving..." : "Approve"}
          </Button>
        </div>
      }
    >
      <PageSection className="grid gap-6 lg:grid-cols-3">
        <Card className="space-y-4 lg:col-span-2">
          <SectionHeader>
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Decision context</h3>
              <p className="text-sm text-slate-600">Case and step identifiers.</p>
            </div>
          </SectionHeader>
          <KeyValueList
            items={[
              { label: "Decision", value: decision.id },
              { label: "Case", value: decision.onboarding_case },
              { label: "Step", value: decision.approval_step },
              { label: "Status", value: decision.decision },
            ]}
          />
        </Card>
        <Card className="space-y-4">
          <h3 className="text-lg font-semibold text-slate-900">Approval history</h3>
          {historyLoading ? (
            <LoadingState label="Loading history" />
          ) : (
            <ApprovalStepTracker
              steps={history.map((item) => ({
                id: item.id,
                label: item.approval_step,
                status:
                  item.decision === "approved"
                    ? "approved"
                    : item.decision === "rejected"
                    ? "rejected"
                    : "pending",
                actor: item.decided_by ?? undefined,
              }))}
            />
          )}
        </Card>
      </PageSection>

      <Modal title="Rejection reason" open={rejectOpen} onClose={() => setRejectOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit(onReject)}>
          <FormField label="Reason" error={errors.comments?.message}>
            <Textarea placeholder="Explain why this case is rejected" {...register("comments")} />
          </FormField>
          <div className="flex justify-end gap-2">
            <Button type="button" variant="secondary" onClick={() => setRejectOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting || rejectMutation.isPending}>
              {rejectMutation.isPending ? "Sending..." : "Send rejection"}
            </Button>
          </div>
        </form>
      </Modal>
    </PageContainer>
  );
}
