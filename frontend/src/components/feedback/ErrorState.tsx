import type { ReactNode } from "react";
import { AlertTriangle } from "lucide-react";

interface ErrorStateProps {
  title: string;
  description: string;
  action?: ReactNode;
}

export function ErrorState({ title, description, action }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-start gap-2 rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-900">
      <div className="flex items-center gap-2">
        <AlertTriangle className="h-4 w-4" />
        <h3 className="text-base font-semibold">{title}</h3>
      </div>
      <p className="text-sm text-red-800">{description}</p>
      {action ? <div className="pt-2">{action}</div> : null}
    </div>
  );
}
