import type { HTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

export function StatGrid({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("grid gap-4 md:grid-cols-2 xl:grid-cols-4", className)} {...props} />
  );
}
