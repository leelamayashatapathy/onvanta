export interface OnboardingCase {
  id: string;
  vendor: string;
  template: string;
  current_stage: string;
  status: string;
  progress_percent: number;
  started_at: string | null;
  submitted_at: string | null;
  completed_at: string | null;
  blocked_reason: string | null;
  created_at: string;
  updated_at: string;
}

export interface OnboardingRequirement {
  id: string;
  case: string;
  document_type: string;
  required: boolean;
  submitted: boolean;
  verified: boolean;
  current_document: string | null;
  due_date: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OnboardingTemplate {
  id: string;
  name: string;
  applies_to_vendor_category: string;
  active: boolean;
  created_at: string;
  updated_at: string;
}
