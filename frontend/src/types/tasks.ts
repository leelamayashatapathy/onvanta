export interface ActionTask {
  id: string;
  organization: string;
  vendor: string | null;
  onboarding_case: string | null;
  task_type: string;
  title: string;
  description?: string;
  assigned_to: string | null;
  due_date: string | null;
  status: string;
  priority: string;
  created_at: string;
  updated_at: string;
}
