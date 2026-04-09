import type { AuthTokens, AuthUser } from "../../types";

const ACCESS_KEY = "onvanta_access_token";
const REFRESH_KEY = "onvanta_refresh_token";
const USER_KEY = "onvanta_user";

export const tokenStorage = {
  getTokens(): AuthTokens | null {
    const access = localStorage.getItem(ACCESS_KEY);
    const refresh = localStorage.getItem(REFRESH_KEY);
    if (!access || !refresh) return null;
    return { access, refresh };
  },
  setTokens(tokens: AuthTokens) {
    localStorage.setItem(ACCESS_KEY, tokens.access);
    localStorage.setItem(REFRESH_KEY, tokens.refresh);
  },
  setAccessToken(access: string) {
    localStorage.setItem(ACCESS_KEY, access);
  },
  clearTokens() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
  getUser(): AuthUser | null {
    const raw = localStorage.getItem(USER_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as AuthUser;
    } catch {
      return null;
    }
  },
  setUser(user: AuthUser) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },
  clearUser() {
    localStorage.removeItem(USER_KEY);
  },
  clearAll() {
    this.clearTokens();
    this.clearUser();
  },
};
