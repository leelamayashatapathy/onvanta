import { PageContainer } from "../../../components/layout/PageContainer";
import { Card } from "../../../components/ui/Card";
import { Checkbox } from "../../../components/forms/Checkbox";

export function NotificationSettingsPage() {
  return (
    <PageContainer
      title="Notification settings"
      description="Control alerts, reminders, and weekly summaries."
    >
      <Card className="space-y-4">
        <Checkbox label="Send expiry alerts 30 days before due date" defaultChecked />
        <Checkbox label="Send daily approval queue digest" defaultChecked />
        <Checkbox label="Send overdue task reminders" />
      </Card>
    </PageContainer>
  );
}
