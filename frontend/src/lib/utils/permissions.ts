import type { UserRole } from "../../types";

const roleRank: Record<UserRole, number> = {
  org_admin: 5,
  procurement_manager: 4,
  compliance_manager: 4,
  approver: 3,
  reviewer: 3,
  read_only: 1,
};

export function canAccess(current: UserRole | undefined, allowed?: UserRole[]) {
  if (!allowed || allowed.length === 0) return true;
  if (!current) return false;
  return allowed.includes(current);
}

export function canEdit(current: UserRole | undefined, minimum: UserRole) {
  if (!current) return false;
  return roleRank[current] >= roleRank[minimum];
}
