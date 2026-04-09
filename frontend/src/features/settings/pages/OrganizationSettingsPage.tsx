import { PageContainer } from "../../../components/layout/PageContainer";
import { FormSection } from "../../../components/forms/FormSection";
import { FormField } from "../../../components/forms/FormField";
import { Input } from "../../../components/ui/Input";
import { Button } from "../../../components/ui/Button";
import { useOrganizationDetail } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";

export function OrganizationSettingsPage() {
  const { data: organization, isLoading, isError } = useOrganizationDetail();

  if (isLoading) {
    return <LoadingState label="Loading organization" />;
  }

  if (isError || !organization) {
    return (
      <ErrorState
        title="Unable to load organization"
        description="Please retry once the backend is available."
      />
    );
  }

  return (
    <PageContainer
      title="Organization profile"
      description="Update organization details and defaults."
      action={<Button disabled>Update via admin</Button>}
    >
      <FormSection>
        <FormField label="Organization name">
          <Input defaultValue={organization.name} disabled />
        </FormField>
        <FormField label="Industry">
          <Input defaultValue={organization.industry} disabled />
        </FormField>
        <FormField label="Size">
          <Input defaultValue={organization.size} disabled />
        </FormField>
        <FormField label="Timezone">
          <Input defaultValue={organization.timezone} disabled />
        </FormField>
      </FormSection>
    </PageContainer>
  );
}
