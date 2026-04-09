import { useMutation } from "@tanstack/react-query";
import { fetchSession, login } from "./api";
import type { LoginPayload, AuthUser, ApiCurrentUser } from "../../types";
import { useAuthStore } from "../../app/store/authStore";
import { tokenStorage } from "../../lib/api/tokens";

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

export function useLogin() {
  const setSession = useAuthStore((state) => state.setSession);

  return useMutation({
    mutationFn: async (payload: LoginPayload) => {
      const tokens = await login(payload);
      tokenStorage.setTokens(tokens);
      const user = await fetchSession();
      return { tokens, user };
    },
    onSuccess: ({ tokens, user }) => {
      setSession({ user: mapUser(user), tokens });
    },
  });
}