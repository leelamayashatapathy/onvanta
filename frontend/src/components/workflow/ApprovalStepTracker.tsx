import { Badge } from "../ui/Badge";

interface ApprovalStep {
  id: string;
  label: string;
  status: "pending" | "approved" | "rejected";
  actor?: string;
}

interface ApprovalStepTrackerProps {
  steps: ApprovalStep[];
}

const toneMap: Record<ApprovalStep["status"], "neutral" | "success" | "error" | "warning"> = {
  pending: "warning",
  approved: "success",
  rejected: "error",
};

export function ApprovalStepTracker({ steps }: ApprovalStepTrackerProps) {
  return (
    <div className="space-y-3">
      {steps.map((step) => (
        <div key={step.id} className="flex items-center justify-between rounded-xl border border-slate-200 px-4 py-2">
          <div>
            <p className="text-sm font-medium text-slate-900">{step.label}</p>
            {step.actor ? <p className="text-xs text-slate-500">{step.actor}</p> : null}
          </div>
          <Badge tone={toneMap[step.status]}>{step.status}</Badge>
        </div>
      ))}
    </div>
  );
}
