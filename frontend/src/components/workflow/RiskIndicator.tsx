import { Badge } from "../ui/Badge";
import type { RiskLevel } from "../../types";
import { formatRiskLabel } from "../../lib/formatters/risk";

const toneMap: Record<RiskLevel, "success" | "warning" | "error"> = {
  low: "success",
  medium: "warning",
  high: "error",
  critical: "error",
};

export function RiskIndicator({ level }: { level: RiskLevel }) {
  return <Badge tone={toneMap[level]}>{formatRiskLabel(level)}</Badge>;
}
