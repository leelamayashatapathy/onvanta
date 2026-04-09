import { PageContainer } from "../../../components/layout/PageContainer";
import { DataTable } from "../../../components/tables/DataTable";
import { Button } from "../../../components/ui/Button";
import { Badge } from "../../../components/ui/Badge";
import { Select } from "../../../components/forms/Select";
import { useMembers } from "../../../lib/api/queries/hooks";
import { useUpdateMemberRole } from "../../../lib/api/queries/mutations";
import { LoadingState } from "../../../components/feedback/LoadingState";
import { ErrorState } from "../../../components/feedback/ErrorState";
import { useState } from "react";

export function MembersPage() {
  const { data: members = [], isLoading, isError } = useMembers();
  const updateRoleMutation = useUpdateMemberRole();
  const [pendingRole, setPendingRole] = useState<Record<string, string>>({});

  return (
    <PageContainer
      title="Members & roles"
      description="Manage organization members and their access level."
      action={<Button variant="secondary">Invite via admin</Button>}
    >
      {isLoading ? <LoadingState label="Loading members" /> : null}
      {isError ? (
        <ErrorState title="Unable to load members" description="Please retry once the backend is available." />
      ) : null}

      {!isLoading && !isError ? (
        <DataTable
          columns={["Member", "Role", "Status", "Action"]}
          rows={members.map((member) => [
            <div key={member.id}>
              <p className="text-sm font-semibold text-slate-900">{member.email}</p>
              <p className="text-xs text-slate-500">{member.user_id}</p>
            </div>,
            <Select
              key={`${member.id}-role`}
              className="w-48"
              value={pendingRole[member.id] ?? member.role}
              onChange={(event) =>
                setPendingRole((prev) => ({ ...prev, [member.id]: event.target.value }))
              }
            >
              <option value="org_admin">Org admin</option>
              <option value="procurement_manager">Procurement manager</option>
              <option value="reviewer">Reviewer</option>
              <option value="approver">Approver</option>
              <option value="compliance_manager">Compliance manager</option>
              <option value="read_only">Read only</option>
            </Select>,
            <Badge key={`${member.id}-status`} tone={member.status === "active" ? "success" : "warning"}>
              {member.status}
            </Badge>,
            <Button
              key={`${member.id}-action`}
              size="sm"
              variant="secondary"
              onClick={() =>
                updateRoleMutation.mutate({
                  memberId: member.id,
                  role: (pendingRole[member.id] ?? member.role) as
                    | "org_admin"
                    | "procurement_manager"
                    | "reviewer"
                    | "approver"
                    | "compliance_manager"
                    | "read_only",
                })
              }
              disabled={updateRoleMutation.isPending}
            >
              Update role
            </Button>,
          ])}
        />
      ) : null}
    </PageContainer>
  );
}
