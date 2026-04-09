import type { PropsWithChildren } from "react";
import { useEffect } from "react";
import { QueryProvider } from "./QueryProvider";
import { useAuthStore } from "../store/authStore";
import { useSession } from "../../lib/api/queries/session";

function SessionGate({ children }: PropsWithChildren) {
  const { isLoading } = useSession();

  if (isLoading) {
    return <div className="flex min-h-screen items-center justify-center text-sm text-slate-500">Loading session...</div>;
  }

  return <>{children}</>;
}

export function AppProviders({ children }: PropsWithChildren) {
  const hydrate = useAuthStore((state) => state.hydrate);

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return (
    <QueryProvider>
      <SessionGate>{children}</SessionGate>
    </QueryProvider>
  );
}
