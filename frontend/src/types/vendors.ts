export type RiskLevel = "low" | "medium" | "high" | "critical";

export interface Vendor {
  id: string;
  vendor_code: string;
  legal_name: string;
  display_name: string;
  vendor_type: string;
  category: string;
  risk_level: RiskLevel;
  owner_user: string | null;
  onboarding_status: string;
  operational_status: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface VendorContact {
  id: string;
  vendor: string;
  name: string;
  email: string;
  phone?: string;
  designation?: string;
  is_primary: boolean;
}
