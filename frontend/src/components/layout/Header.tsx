import { Bell, Search, ChevronDown } from "lucide-react";
import { useLocation } from "react-router-dom";
import { ROUTE_TITLES } from "../../app/router/routes";
import { IconButton } from "../ui/IconButton";
import { useAuthStore } from "../../app/store/authStore";

const fallbackTitles: Array<{ prefix: string; label: string }> = [
  { prefix: "/app/vendors/", label: "Vendor Profile" },
  { prefix: "/app/onboarding/", label: "Onboarding Case" },
  { prefix: "/app/documents/", label: "Document" },
  { prefix: "/app/approvals/", label: "Approval Review" },
  { prefix: "/app/tasks/", label: "Task" },
];

export function Header() {
  const location = useLocation();
  const user = useAuthStore((state) => state.user);

  const title =
    ROUTE_TITLES[location.pathname] ??
    fallbackTitles.find((item) => location.pathname.startsWith(item.prefix))?.label ??
    "Onvanta";

  return (
    <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="flex items-center justify-between gap-4 px-6 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Workspace</p>
          <h1 className="text-xl font-semibold text-slate-900">{title}</h1>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-500 md:flex">
            <Search className="h-4 w-4" />
            <span>Search vendors, cases, documents</span>
          </div>
          <IconButton aria-label="Notifications">
            <Bell className="h-4 w-4 text-slate-600" />
          </IconButton>
          <button className="flex items-center gap-2 rounded-xl border border-slate-200 px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-900 text-xs font-semibold text-white">
              {user?.fullName?.[0] ?? "U"}
            </div>
            <div className="hidden sm:block">
              <p className="text-sm font-medium text-slate-900">{user?.fullName ?? "User"}</p>
              <p className="text-xs text-slate-500">{user?.organizationName ?? "Organization"}</p>
            </div>
            <ChevronDown className="h-4 w-4 text-slate-500" />
          </button>
        </div>
      </div>
    </header>
  );
}
