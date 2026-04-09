export interface OrganizationDetail {
  id: string;
  name: string;
  slug: string;
  industry: string;
  size: string;
  timezone: string;
  settings_json: Record<string, unknown>;
}
