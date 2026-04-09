import type { HTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

export function SectionHeader({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("flex flex-wrap items-start justify-between gap-3", className)}
      {...props}
    />
  );
}
