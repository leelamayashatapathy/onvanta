import { cn } from "../../lib/utils/cn";

interface ProgressBarProps {
  value: number;
  label?: string;
  tone?: "neutral" | "success" | "warning" | "error";
}

const toneStyles: Record<NonNullable<ProgressBarProps["tone"]>, string> = {
  neutral: "bg-slate-900",
  success: "bg-emerald-500",
  warning: "bg-amber-500",
  error: "bg-red-500",
};

export function ProgressBar({ value, label, tone = "neutral" }: ProgressBarProps) {
  const safeValue = Math.min(100, Math.max(0, value));

  return (
    <div className="space-y-2">
      {label ? <p className="text-xs font-medium text-slate-600">{label}</p> : null}
      <div className="h-2 w-full rounded-full bg-slate-100">
        <div
          className={cn("h-2 rounded-full transition-all", toneStyles[tone])}
          style={{ width: `${safeValue}%` }}
        />
      </div>
    </div>
  );
}
