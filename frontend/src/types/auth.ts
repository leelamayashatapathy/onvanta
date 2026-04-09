export type UserRole =
  | "org_admin"
  | "procurement_manager"
  | "reviewer"
  | "approver"
  | "compliance_manager"
  | "read_only";

export interface AuthUser {
  id: string;
  email: string;
  fullName: string;
  role: UserRole;
  organizationId: string;
  organizationName: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface ApiLoginResponse {
  access: string;
  refresh: string;
}

export interface ApiMembership {
  organization_id: string;
  organization_name: string;
  role: UserRole;
  status: string;
}

export interface ApiCurrentUser {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  memberships: ApiMembership[];
}
