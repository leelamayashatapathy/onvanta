import type { RiskLevel } from "../../types";

export function formatRiskLabel(level: RiskLevel) {
  switch (level) {
    case "low":
      return "Low";
    case "medium":
      return "Medium";
    case "high":
      return "High";
    case "critical":
      return "Critical";
    default:
      return "Unknown";
  }
}
