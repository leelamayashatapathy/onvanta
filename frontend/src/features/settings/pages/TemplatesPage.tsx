import { PageContainer } from "../../../components/layout/PageContainer";
import { DataTable } from "../../../components/tables/DataTable";
import { Button } from "../../../components/ui/Button";
import { Modal } from "../../../components/ui/Modal";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { FormField } from "../../../components/forms/FormField";
import { Input } from "../../../components/ui/Input";
import { Checkbox } from "../../../components/forms/Checkbox";
import { useCreateTemplate } from "../../../lib/api/queries/mutations";
import { useTemplates } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";

const schema = z.object({
  name: z.string().min(2, "Name is required"),
  applies_to_vendor_category: z.string().optional(),
  active: z.boolean().optional(),
});

type FormValues = z.infer<typeof schema>;

export function TemplatesPage() {
  const { data: templates = [], isLoading, isError } = useTemplates();
  const createMutation = useCreateTemplate();
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
      applies_to_vendor_category: values.applies_to_vendor_category ?? "",
      active: Boolean(values.active),
    });
    setOpen(false);
  };

  return (
    <PageContainer
      title="Onboarding templates"
      description="Configure requirement bundles by vendor type."
      action={<Button onClick={() => setOpen(true)}>Create template</Button>}
    >
      {isLoading ? <LoadingState label="Loading templates" /> : null}
      {isError ? (
        <ErrorState title="Unable to load templates" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <DataTable
          columns={["Template", "Applies to", "Active"]}
          rows={templates.map((item) => [
            <span key={item.id} className="text-sm font-semibold text-slate-900">
              {item.name}
            </span>,
            <span key={`${item.id}-desc`} className="text-sm text-slate-600">
              {item.applies_to_vendor_category || "All"}
            </span>,
            <span key={`${item.id}-req`} className="text-sm text-slate-600">
              {item.active ? "Yes" : "No"}
            </span>,
          ])}
        />
      ) : null}

      <Modal title="Create template" open={open} onClose={() => setOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Name" error={errors.name?.message}>
            <Input placeholder="High-risk vendor" {...register("name")} />
          </FormField>
          <FormField label="Applies to vendor category" error={errors.applies_to_vendor_category?.message}>
            <Input placeholder="Security" {...register("applies_to_vendor_category")} />
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
