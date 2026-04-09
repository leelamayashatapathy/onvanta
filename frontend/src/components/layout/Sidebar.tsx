import { NavLink } from "react-router-dom";
import { cn } from "../../lib/utils/cn";
import { NAV_ITEMS } from "../../app/router/routes";
import { useAuthStore } from "../../app/store/authStore";
import { useUiStore } from "../../app/store/uiStore";
import { ChevronLeft, ChevronRight } from "lucide-react";

export function Sidebar() {
  const user = useAuthStore((state) => state.user);
  const { sidebarCollapsed, toggleSidebar } = useUiStore();

  const navItems = NAV_ITEMS.filter((item) => {
    if (!item.roles || !user?.role) return true;
    return item.roles.includes(user.role);
  });

  return (
    <aside
      className={cn(
        "flex min-h-screen flex-col border-r border-slate-200 bg-white px-4 py-6 transition-all",
        sidebarCollapsed ? "w-20" : "w-64"
      )}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-600 text-white font-semibold">
            O
          </div>
          {!sidebarCollapsed ? (
            <div>
              <p className="text-sm font-semibold text-slate-900">Onvanta</p>
              <p className="text-xs text-slate-500">Vendor OS</p>
            </div>
          ) : null}
        </div>
        <button
          className="rounded-xl border border-slate-200 p-1 text-slate-500 hover:bg-slate-100"
          onClick={toggleSidebar}
          aria-label="Toggle sidebar"
        >
          {sidebarCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      <nav className="mt-8 flex flex-1 flex-col gap-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition",
                  isActive
                    ? "bg-blue-50 text-blue-700"
                    : "text-slate-600 hover:bg-slate-100"
                )
              }
            >
              <Icon className="h-4 w-4" />
              {!sidebarCollapsed ? <span>{item.label}</span> : null}
            </NavLink>
          );
        })}
      </nav>

      {!sidebarCollapsed ? (
        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-3 text-xs text-slate-600">
          <p className="font-medium text-slate-700">Compliance snapshot</p>
          <p className="mt-1">3 vendors need attention</p>
          <p className="mt-1 text-slate-500">Next expiry in 6 days</p>
        </div>
      ) : null}
    </aside>
  );
}
