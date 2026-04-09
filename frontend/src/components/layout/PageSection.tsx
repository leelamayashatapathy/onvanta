import type { HTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

export function PageSection({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <section className={cn("space-y-4", className)} {...props} />
  );
}
