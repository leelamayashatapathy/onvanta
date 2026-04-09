import { useQuery } from "@tanstack/react-query";
import { fetchSession } from "../../../features/auth/api";
import { QUERY_KEYS } from "./keys";
import { useAuthStore } from "../../../app/store/authStore";
import type { AuthUser, ApiCurrentUser } from "../../../types";

function mapUser(apiUser: ApiCurrentUser): AuthUser {
  const membership = apiUser.memberships[0];
  return {
    id: apiUser.id,
    email: apiUser.email,
    fullName: `${apiUser.first_name} ${apiUser.last_name}`.trim(),
    role: membership?.role ?? "read_only",
    organizationId: membership?.organization_id ?? "",
    organizationName: membership?.organization_name ?? "Organization",
  };
}

export function useSession() {
  const setSession = useAuthStore((state) => state.setSession);
  const tokens = useAuthStore((state) => state.tokens);

  return useQuery({
    queryKey: QUERY_KEYS.session,
    queryFn: fetchSession,
    enabled: Boolean(tokens?.access),
    onSuccess: (user) => {
      if (!tokens) return;
      setSession({ user: mapUser(user), tokens });
    },
  });
}
