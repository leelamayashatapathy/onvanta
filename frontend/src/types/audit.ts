export interface AuditEvent {
  id: string;
  organization: string;
  actor_user: string | null;
  actor_type: string;
  entity_type: string;
  entity_id: string;
  action: string;
  source: string;
  old_data_json: Record<string, unknown> | null;
  new_data_json: Record<string, unknown> | null;
  created_at: string;
}
