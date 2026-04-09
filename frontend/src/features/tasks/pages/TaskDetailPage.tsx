import { PageContainer } from "../../../components/layout/PageContainer";
import { PageSection } from "../../../components/layout/PageSection";
import { Card } from "../../../components/ui/Card";
import { Button } from "../../../components/ui/Button";
import { KeyValueList } from "../../../components/ui/KeyValueList";
import { useCompleteTask } from "../../../lib/api/queries/mutations";
import { useParams } from "react-router-dom";
import { useTasks } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";

export function TaskDetailPage() {
  const { taskId = "" } = useParams();
  const { data: tasks = [] } = useTasks();
  const task = tasks.find((item) => item.id === taskId);
  const updateMutation = useCompleteTask();

  if (!task) {
    return <LoadingState label="Loading task" />;
  }

  return (
    <PageContainer
      title="Task detail"
      description="Track task ownership, due date, and status."
      action={
        <div className="flex gap-2">
          <Button
            onClick={() => updateMutation.mutate(taskId)}
            disabled={updateMutation.isPending}
          >
            {updateMutation.isPending ? "Updating..." : "Mark complete"}
          </Button>
        </div>
      }
    >
      <PageSection className="grid gap-6 lg:grid-cols-3">
        <Card className="space-y-4 lg:col-span-2">
          <h3 className="text-lg font-semibold text-slate-900">{task.title}</h3>
          <p className="text-sm text-slate-600">
            {task.description ?? "No description provided."}
          </p>
        </Card>
        <Card className="space-y-4">
          <h3 className="text-lg font-semibold text-slate-900">Task metadata</h3>
          <KeyValueList
            items={[
              { label: "Vendor", value: task.vendor ?? "—" },
              { label: "Assignee", value: task.assigned_to ?? "—" },
              { label: "Due", value: task.due_date ?? "—" },
              { label: "Status", value: task.status },
            ]}
          />
        </Card>
      </PageSection>
    </PageContainer>
  );
}
