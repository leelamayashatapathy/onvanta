import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { PageContainer } from "../../../components/layout/PageContainer";
import { FormSection } from "../../../components/forms/FormSection";
import { FormField } from "../../../components/forms/FormField";
import { FormActions } from "../../../components/forms/FormActions";
import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/forms/Select";
import { Textarea } from "../../../components/forms/Textarea";
import { Button } from "../../../components/ui/Button";
import { useCreateVendor } from "../../../lib/api/queries/mutations";
import { useNavigate } from "react-router-dom";

const schema = z.object({
  vendor_code: z.string().min(2, "Vendor code is required"),
  legal_name: z.string().min(2, "Legal name is required"),
  display_name: z.string().min(2, "Display name is required"),
  vendor_type: z.string().optional(),
  category: z.string().optional(),
  risk_level: z.enum(["low", "medium", "high", "critical"]).optional(),
  owner_user: z.string().optional(),
  notes: z.string().optional(),
});

type FormValues = z.infer<typeof schema>;

export function VendorCreatePage() {
  const navigate = useNavigate();
  const createVendorMutation = useCreateVendor();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isValid },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    mode: "onChange",
  });

  const onSubmit = async (values: FormValues) => {
    const created = await createVendorMutation.mutateAsync({
      ...values,
      owner_user: values.owner_user || null,
      vendor_type: values.vendor_type || "",
      category: values.category || "",
    });
    navigate(`/app/vendors/${created.id}`);
  };

  return (
    <PageContainer
      title="Create vendor"
      description="Capture vendor profile, risk, and ownership to start onboarding."
    >
      <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
        <FormSection>
          <FormField label="Vendor code" error={errors.vendor_code?.message}>
            <Input placeholder="VEN-001" {...register("vendor_code")} />
          </FormField>
          <FormField label="Legal name" error={errors.legal_name?.message}>
            <Input placeholder="Northwind Logistics LLC" {...register("legal_name")} />
          </FormField>
          <FormField label="Display name" error={errors.display_name?.message}>
            <Input placeholder="Northwind Logistics" {...register("display_name")} />
          </FormField>
        </FormSection>

        <FormSection>
          <FormField label="Vendor type" error={errors.vendor_type?.message}>
            <Input placeholder="Logistics" {...register("vendor_type")} />
          </FormField>
          <FormField label="Category" error={errors.category?.message}>
            <Input placeholder="Logistics" {...register("category")} />
          </FormField>
          <FormField label="Risk level" error={errors.risk_level?.message}>
            <Select defaultValue="" {...register("risk_level")}>
              <option value="">Select risk</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </Select>
          </FormField>
          <FormField label="Owner user ID" error={errors.owner_user?.message}>
            <Input placeholder="UUID of owner" {...register("owner_user")} />
          </FormField>
          <FormField label="Notes" error={errors.notes?.message} helper="Optional onboarding context.">
            <Textarea placeholder="Key services, scope, compliance notes" {...register("notes")} />
          </FormField>
        </FormSection>

        <FormActions>
          <Button variant="secondary" type="button" onClick={() => navigate("/app/vendors")}>
            Cancel
          </Button>
          <Button type="submit" disabled={!isValid || isSubmitting || createVendorMutation.isPending}>
            {createVendorMutation.isPending ? "Saving..." : "Create vendor"}
          </Button>
        </FormActions>
      </form>
    </PageContainer>
  );
}
