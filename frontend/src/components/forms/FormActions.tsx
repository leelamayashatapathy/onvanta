import type { HTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

export function FormActions({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("flex flex-wrap items-center justify-end gap-3", className)} {...props} />
  );
}
