import { Loader2 } from "lucide-react";

interface LoadingStateProps {
  label?: string;
}

export function LoadingState({ label = "Loading..." }: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 rounded-2xl border border-slate-200 bg-white p-8 text-sm text-slate-600">
      <Loader2 className="h-5 w-5 animate-spin text-slate-500" />
      <span>{label}</span>
    </div>
  );
}
