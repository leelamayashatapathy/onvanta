import { PageContainer } from "../../../components/layout/PageContainer";
import { Card } from "../../../components/ui/Card";
import { Button } from "../../../components/ui/Button";
import { Modal } from "../../../components/ui/Modal";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { FormField } from "../../../components/forms/FormField";
import { Input } from "../../../components/ui/Input";
import { Checkbox } from "../../../components/forms/Checkbox";
import { useApprovalFlows } from "../../../lib/api/queries/hooks";
import { useCreateApprovalFlow } from "../../../lib/api/queries/mutations";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";

const schema = z.object({
  name: z.string().min(2, "Name is required"),
  scope: z.string().min(2, "Scope is required"),
  active: z.boolean().optional(),
});

type FormValues = z.infer<typeof schema>;

export function ApprovalFlowsPage() {
  const { data: flows = [], isLoading, isError } = useApprovalFlows();
  const createMutation = useCreateApprovalFlow();
  const [open, setOpen] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (values: FormValues) => {
    await createMutation.mutateAsync({
      name: values.name,
      scope: values.scope,
      active: Boolean(values.active),
    });
    setOpen(false);
  };

  return (
    <PageContainer
      title="Approval flows"
      description="Define multi-step approval routing by vendor risk."
      action={<Button onClick={() => setOpen(true)}>Create flow</Button>}
    >
      {isLoading ? <LoadingState label="Loading approval flows" /> : null}
      {isError ? (
        <ErrorState title="Unable to load flows" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <div className="grid gap-4 md:grid-cols-2">
          {flows.map((flow) => (
            <Card key={flow.id} className="space-y-2">
              <p className="text-sm font-semibold text-slate-900">{flow.name}</p>
              <p className="text-sm text-slate-600">Scope: {flow.scope}</p>
              <p className="text-xs text-slate-500">{flow.active ? "Active" : "Inactive"}</p>
            </Card>
          ))}
        </div>
      ) : null}

      <Modal title="Create approval flow" open={open} onClose={() => setOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Name" error={errors.name?.message}>
            <Input placeholder="Standard approval" {...register("name")} />
          </FormField>
          <FormField label="Scope" error={errors.scope?.message}>
            <Input placeholder="default" {...register("scope")} />
          </FormField>
          <Checkbox label="Active" {...register("active")} />
          <div className="flex justify-end gap-2">
            <Button type="button" variant="secondary" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting || createMutation.isPending}>
              {createMutation.isPending ? "Saving..." : "Create"}
            </Button>
          </div>
        </form>
      </Modal>
    </PageContainer>
  );
}
