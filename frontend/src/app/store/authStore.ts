import { create } from "zustand";
import type { AuthTokens, AuthUser } from "../../types";
import { tokenStorage } from "../../lib/api/tokens";

interface AuthState {
  user: AuthUser | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  hydrate: () => void;
  setSession: (payload: { user: AuthUser; tokens: AuthTokens }) => void;
  clearSession: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  tokens: null,
  isAuthenticated: false,
  hydrate: () => {
    const tokens = tokenStorage.getTokens();
    const user = tokenStorage.getUser();
    set({
      tokens,
      user,
      isAuthenticated: Boolean(tokens?.access && user),
    });
  },
  setSession: ({ user, tokens }) => {
    tokenStorage.setTokens(tokens);
    tokenStorage.setUser(user);
    set({ user, tokens, isAuthenticated: true });
  },
  clearSession: () => {
    tokenStorage.clearAll();
    set({ user: null, tokens: null, isAuthenticated: false });
  },
}));
