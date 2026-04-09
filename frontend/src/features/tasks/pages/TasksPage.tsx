import { PageContainer } from "../../../components/layout/PageContainer";
import { FilterBar } from "../../../components/tables/FilterBar";
import { DataTable } from "../../../components/tables/DataTable";
import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/forms/Select";
import { Badge } from "../../../components/ui/Badge";
import { Link } from "react-router-dom";
import { useTasks } from "../../../lib/api/queries/hooks";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";

export function TasksPage() {
  const { data: tasks = [], isLoading, isError } = useTasks();

  return (
    <PageContainer
      title="Tasks"
      description="Operational follow-ups across onboarding and renewals."
    >
      <FilterBar>
        <div className="w-full max-w-xs">
          <Input placeholder="Search tasks" />
        </div>
        <Select className="w-48" defaultValue="">
          <option value="">All statuses</option>
          <option value="open">Open</option>
          <option value="done">Done</option>
        </Select>
      </FilterBar>

      {isLoading ? <LoadingState label="Loading tasks" /> : null}
      {isError ? (
        <ErrorState title="Unable to load tasks" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <DataTable
          columns={["Task", "Vendor", "Due", "Assignee", "Priority", "Action"]}
          rows={tasks.map((task) => [
            <div key={task.id}>
              <p className="text-sm font-semibold text-slate-900">{task.title}</p>
              <p className="text-xs text-slate-500">{task.task_type}</p>
            </div>,
            <span key={`${task.id}-vendor`} className="text-sm text-slate-600">
              {task.vendor ?? "—"}
            </span>,
            <span key={`${task.id}-due`} className="text-sm text-slate-600">
              {task.due_date ?? "—"}
            </span>,
            <span key={`${task.id}-owner`} className="text-sm text-slate-600">
              {task.assigned_to ?? "—"}
            </span>,
            <Badge key={`${task.id}-priority`} tone={task.priority === "high" ? "error" : "warning"}>
              {task.priority}
            </Badge>,
            <Link key={`${task.id}-action`} to={`/app/tasks/${task.id}`} className="text-sm font-medium text-blue-600">
              View task
            </Link>,
          ])}
        />
      ) : null}
    </PageContainer>
  );
}
