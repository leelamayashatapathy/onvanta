import type { HTMLAttributes } from "react";
import { Badge } from "./Badge";

interface StatusBadgeProps extends HTMLAttributes<HTMLSpanElement> {
  status: string;
  tone?: "neutral" | "success" | "warning" | "error" | "info";
}

export function StatusBadge({ status, tone = "neutral", ...props }: StatusBadgeProps) {
  return (
    <Badge tone={tone} {...props}>
      {status}
    </Badge>
  );
}
