import { Badge } from "../ui/Badge";

interface ChecklistItemProps {
  title: string;
  status: "missing" | "submitted" | "approved" | "rejected";
  owner: string;
  dueDate?: string;
}

const toneMap: Record<ChecklistItemProps["status"], "neutral" | "success" | "warning" | "error"> = {
  missing: "warning",
  submitted: "info",
  approved: "success",
  rejected: "error",
};

export function ChecklistItem({ title, status, owner, dueDate }: ChecklistItemProps) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3">
      <div>
        <p className="text-sm font-semibold text-slate-900">{title}</p>
        <p className="text-xs text-slate-500">Owner: {owner}</p>
      </div>
      <div className="flex items-center gap-3">
        {dueDate ? <span className="text-xs text-slate-500">Due {dueDate}</span> : null}
        <Badge tone={toneMap[status]}>{status}</Badge>
      </div>
    </div>
  );
}
