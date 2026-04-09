import { PageContainer } from "../../../components/layout/PageContainer";
import { FilterBar } from "../../../components/tables/FilterBar";
import { DataTable } from "../../../components/tables/DataTable";
import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/forms/Select";
import { Badge } from "../../../components/ui/Badge";
import { Link } from "react-router-dom";
import { formatDate } from "../../../lib/formatters/date";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";
import { Button } from "../../../components/ui/Button";
import { Modal } from "../../../components/ui/Modal";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { FormField } from "../../../components/forms/FormField";
import { FileUpload } from "../../../components/forms/FileUpload";
import { useUploadDocument } from "../../../lib/api/queries/mutations";
import { useVendorDocuments } from "../../../lib/api/queries/hooks";

const uploadSchema = z.object({
  vendor_id: z.string().min(1, "Vendor ID is required"),
  document_type_id: z.string().min(1, "Document type ID is required"),
  issue_date: z.string().optional(),
  expiry_date: z.string().optional(),
  file: z.instanceof(File, { message: "File is required" }),
});

type UploadFormValues = z.infer<typeof uploadSchema>;

export function DocumentListPage() {
  const [open, setOpen] = useState(false);
  const [vendorId, setVendorId] = useState("");
  const { data: documents = [], isLoading, isError } = useVendorDocuments(vendorId);
  const uploadMutation = useUploadDocument();

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<UploadFormValues>({
    resolver: zodResolver(uploadSchema),
  });

  const onSubmit = async (values: UploadFormValues) => {
    await uploadMutation.mutateAsync(values);
    setOpen(false);
  };

  return (
    <PageContainer
      title="Documents"
      description="Review vendor documents, status, and expiries."
      action={
        <Button onClick={() => setOpen(true)}>
          Upload document
        </Button>
      }
    >
      <FilterBar>
        <div className="w-full max-w-xs">
          <Input
            placeholder="Vendor ID"
            value={vendorId}
            onChange={(event) => setVendorId(event.target.value)}
          />
        </div>
        <Select className="w-48" defaultValue="">
          <option value="">All statuses</option>
          <option value="under_review">In review</option>
          <option value="active">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="expired">Expired</option>
        </Select>
      </FilterBar>

      {isLoading ? <LoadingState label="Loading documents" /> : null}
      {isError ? (
        <ErrorState title="Unable to load documents" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <DataTable
          columns={["Document", "Vendor", "Status", "Expiry", "Uploaded", "Action"]}
          rows={documents.map((doc) => [
            <div key={doc.id}>
              <p className="text-sm font-semibold text-slate-900">{doc.document_type}</p>
              <p className="text-xs text-slate-500">{doc.original_name}</p>
            </div>,
            <span key={`${doc.id}-vendor`} className="text-sm text-slate-600">
              {doc.vendor}
            </span>,
            <Badge key={`${doc.id}-status`} tone={doc.status === "active" ? "success" : "warning"}>
              {doc.status}
            </Badge>,
            <span key={`${doc.id}-expiry`} className="text-sm text-slate-600">
              {doc.expiry_date ? formatDate(doc.expiry_date) : "N/A"}
            </span>,
            <span key={`${doc.id}-owner`} className="text-sm text-slate-600">
              {doc.uploaded_by ?? "—"}
            </span>,
            <Link key={`${doc.id}-action`} to={`/app/documents/${doc.id}`} className="text-sm font-medium text-blue-600">
              Review
            </Link>,
          ])}
        />
      ) : null}

      <Modal title="Upload document" open={open} onClose={() => setOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Vendor ID" error={errors.vendor_id?.message}>
            <Input {...register("vendor_id")} placeholder="UUID of vendor" />
          </FormField>
          <FormField label="Document type ID" error={errors.document_type_id?.message}>
            <Input {...register("document_type_id")} placeholder="UUID of document type" />
          </FormField>
          <FormField label="Issue date" error={errors.issue_date?.message}>
            <Input type="date" {...register("issue_date")} />
          </FormField>
          <FormField label="Expiry date" error={errors.expiry_date?.message}>
            <Input type="date" {...register("expiry_date")} />
          </FormField>
          <FormField label="File" error={errors.file?.message}>
            <FileUpload
              label="Select document file"
              onChange={(event) => {
                const file = event.target.files?.[0];
                if (file) {
                  setValue("file", file, { shouldValidate: true });
                }
              }}
            />
          </FormField>
          <div className="flex justify-end gap-2">
            <Button type="button" variant="secondary" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting || uploadMutation.isPending}>
              {uploadMutation.isPending ? "Uploading..." : "Upload"}
            </Button>
          </div>
        </form>
      </Modal>
    </PageContainer>
  );
}
