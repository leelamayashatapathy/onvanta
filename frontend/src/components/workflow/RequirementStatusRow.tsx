import { Badge } from "../ui/Badge";

interface RequirementStatusRowProps {
  title: string;
  status: "missing" | "submitted" | "approved" | "rejected";
  owner: string;
  dueDate?: string;
}

const toneMap: Record<RequirementStatusRowProps["status"], "warning" | "info" | "success" | "error"> = {
  missing: "warning",
  submitted: "info",
  approved: "success",
  rejected: "error",
};

export function RequirementStatusRow({ title, status, owner, dueDate }: RequirementStatusRowProps) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 py-3">
      <div>
        <p className="text-sm font-medium text-slate-900">{title}</p>
        <p className="text-xs text-slate-500">Owner: {owner}</p>
      </div>
      <div className="flex items-center gap-3">
        {dueDate ? <span className="text-xs text-slate-500">Due {dueDate}</span> : null}
        <Badge tone={toneMap[status]}>{status}</Badge>
      </div>
    </div>
  );
}
