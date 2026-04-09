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
import { useCreateDocumentType } from "../../../lib/api/queries/mutations";
import { useDocumentTypes } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";
import { Select } from "../../../components/forms/Select";
import { Textarea } from "../../../components/forms/Textarea";

const schema = z.object({
  code: z.string().min(2, "Code is required"),
  name: z.string().min(2, "Name is required"),
  category: z.string().optional(),
  description: z.string().optional(),
  is_mandatory: z.boolean().optional(),
  has_expiry: z.boolean().optional(),
  expiry_warning_days: z.coerce.number().optional(),
  criticality: z.enum(["low", "medium", "high", "critical"]),
});

type FormValues = z.infer<typeof schema>;

export function DocumentTypesPage() {
  const { data: types = [], isLoading, isError } = useDocumentTypes();
  const createMutation = useCreateDocumentType();
  const [open, setOpen] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { criticality: "medium" },
  });

  const onSubmit = async (values: FormValues) => {
    await createMutation.mutateAsync({
      ...values,
      category: values.category ?? "",
      description: values.description ?? "",
      is_mandatory: Boolean(values.is_mandatory),
      has_expiry: Boolean(values.has_expiry),
      expiry_warning_days: values.expiry_warning_days,
      applies_to_vendor_type: "",
      allowed_extensions: ["pdf"],
      max_file_size_mb: 10,
    });
    setOpen(false);
  };

  return (
    <PageContainer
      title="Document types"
      description="Define required documents and renewal cadence."
      action={<Button onClick={() => setOpen(true)}>Add document type</Button>}
    >
      {isLoading ? <LoadingState label="Loading document types" /> : null}
      {isError ? (
        <ErrorState title="Unable to load document types" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <DataTable
          columns={["Code", "Name", "Category", "Mandatory", "Criticality"]}
          rows={types.map((item) => [
            <span key={item.id} className="text-sm font-semibold text-slate-900">
              {item.code}
            </span>,
            <span key={`${item.id}-name`} className="text-sm text-slate-600">
              {item.name}
            </span>,
            <span key={`${item.id}-category`} className="text-sm text-slate-600">
              {item.category || "—"}
            </span>,
            <span key={`${item.id}-required`} className="text-sm text-slate-600">
              {item.is_mandatory ? "Yes" : "No"}
            </span>,
            <span key={`${item.id}-crit`} className="text-sm text-slate-600">
              {item.criticality}
            </span>,
          ])}
        />
      ) : null}

      <Modal title="Add document type" open={open} onClose={() => setOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Code" error={errors.code?.message}>
            <Input placeholder="COI" {...register("code")} />
          </FormField>
          <FormField label="Name" error={errors.name?.message}>
            <Input placeholder="Insurance COI" {...register("name")} />
          </FormField>
          <FormField label="Category" error={errors.category?.message}>
            <Input placeholder="Insurance" {...register("category")} />
          </FormField>
          <FormField label="Description" error={errors.description?.message}>
            <Textarea placeholder="Certificate of insurance" {...register("description")} />
          </FormField>
          <FormField label="Criticality" error={errors.criticality?.message}>
            <Select defaultValue="medium" {...register("criticality")}>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </Select>
          </FormField>
          <FormField label="Expiry warning (days)" error={errors.expiry_warning_days?.message}>
            <Input type="number" {...register("expiry_warning_days")} />
          </FormField>
          <Checkbox label="Mandatory" {...register("is_mandatory")} />
          <Checkbox label="Has expiry" {...register("has_expiry")} />
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
