import { Outlet } from "react-router-dom";

export function AuthLayout() {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col gap-8 px-6 py-12 lg:flex-row lg:items-center">
        <div className="flex-1">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
            Vendor Onboarding + Document OS
          </div>
          <h1 className="mt-5 text-3xl font-semibold text-slate-900 lg:text-4xl">
            Onvanta keeps vendor compliance visible and predictable.
          </h1>
          <p className="mt-4 max-w-xl text-base text-slate-600">
            Centralize onboarding, document collection, approvals, and renewal tracking in a
            single workspace for procurement, compliance, and finance teams.
          </p>
          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            {[
              "Unified vendor risk visibility",
              "Document expiry early warnings",
              "Approval and audit readiness",
              "Clear ownership and follow-ups",
            ].map((item) => (
              <div key={item} className="rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-700">
                {item}
              </div>
            ))}
          </div>
        </div>
        <div className="w-full max-w-md">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
