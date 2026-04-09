import type { HTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

export function FormSection({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("space-y-4 rounded-2xl border border-slate-200 bg-white p-5", className)} {...props} />
  );
}
