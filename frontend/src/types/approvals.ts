export interface ApprovalDecision {
  id: string;
  onboarding_case: string;
  approval_step: string;
  decision: string;
  decided_by: string | null;
  decided_at: string | null;
  comments: string;
  created_at: string;
  updated_at: string;
}

export interface ApprovalFlow {
  id: string;
  name: string;
  scope: string;
  active: boolean;
  created_at: string;
  updated_at: string;
}
