import type { RiskLevel } from "./vendors";

export interface DocumentType {
  id: string;
  code: string;
  name: string;
  description: string;
  category: string;
  is_mandatory: boolean;
  has_expiry: boolean;
  expiry_warning_days: number | null;
  criticality: RiskLevel;
  applies_to_vendor_type: string;
  allowed_extensions: string[];
  max_file_size_mb: number | null;
}
