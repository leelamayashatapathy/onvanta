import { PageContainer } from "../../../components/layout/PageContainer";
import { PageSection } from "../../../components/layout/PageSection";
import { SectionHeader } from "../../../components/layout/SectionHeader";
import { Card } from "../../../components/ui/Card";
import { Badge } from "../../../components/ui/Badge";
import { Button } from "../../../components/ui/Button";
import { KeyValueList } from "../../../components/ui/KeyValueList";
import { Modal } from "../../../components/ui/Modal";
import { useState } from "react";
import { useParams } from "react-router-dom";
import { useDocument } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";
import { useApproveDocument, useRejectDocument } from "../../../lib/api/queries/mutations";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { FormField } from "../../../components/forms/FormField";
import { Textarea } from "../../../components/forms/Textarea";

const rejectSchema = z.object({
  rejection_reason: z.string().min(4, "Reason is required"),
});

type RejectFormValues = z.infer<typeof rejectSchema>;

export function DocumentDetailPage() {
  const [rejectOpen, setRejectOpen] = useState(false);
  const { documentId = "" } = useParams();
  const { data: document, isLoading, isError } = useDocument(documentId);
  const approveMutation = useApproveDocument();
  const rejectMutation = useRejectDocument();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RejectFormValues>({
    resolver: zodResolver(rejectSchema),
  });

  if (isLoading) {
    return <LoadingState label="Loading document" />;
  }

  if (isError || !document) {
    return (
      <ErrorState
        title="Unable to load document"
        description="Please check the document ID or try again."
      />
    );
  }

  const onReject = async (values: RejectFormValues) => {
    await rejectMutation.mutateAsync({ documentId: document.id, rejection_reason: values.rejection_reason });
    setRejectOpen(false);
  };

  return (
    <PageContainer
      title="Document review"
      description="Review metadata, decision, and version history."
      action={
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => setRejectOpen(true)}>
            Reject
          </Button>
          <Button
            onClick={() => approveMutation.mutate(document.id)}
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
              <h3 className="text-lg font-semibold text-slate-900">Document metadata</h3>
              <p className="text-sm text-slate-600">Verify details before approval.</p>
            </div>
            <Badge tone="warning">{document.status}</Badge>
          </SectionHeader>
          <KeyValueList
            items={[
              { label: "Type", value: document.document_type },
              { label: "File name", value: document.original_name },
              { label: "Issue date", value: document.issue_date ?? "N/A" },
              { label: "Expiry", value: document.expiry_date ?? "N/A" },
              { label: "Uploaded by", value: document.uploaded_by ?? "—" },
              { label: "Version", value: `v${document.version}` },
            ]}
          />
        </Card>
        <Card className="space-y-4">
          <h3 className="text-lg font-semibold text-slate-900">Version history</h3>
          <div className="space-y-3 text-sm text-slate-600">
            <div className="rounded-xl border border-slate-200 px-3 py-2">v{document.version} uploaded</div>
            <div className="rounded-xl border border-slate-200 px-3 py-2">No prior versions</div>
          </div>
        </Card>
      </PageSection>

      <Modal title="Rejection reason" open={rejectOpen} onClose={() => setRejectOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit(onReject)}>
          <FormField label="Reason" error={errors.rejection_reason?.message}>
            <Textarea placeholder="Explain why the document is rejected" {...register("rejection_reason")} />
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
