import type { ReactNode } from "react";
import { X } from "lucide-react";

interface DrawerProps {
  title: string;
  open: boolean;
  onClose: () => void;
  children: ReactNode;
}

export function Drawer({ title, open, onClose, children }: DrawerProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex">
      <div className="flex-1 bg-slate-900/30" onClick={onClose} />
      <div className="w-full max-w-md bg-white p-6 shadow-card">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
          <button className="rounded-xl p-1 hover:bg-slate-100" onClick={onClose} aria-label="Close">
            <X className="h-4 w-4" />
          </button>
        </div>
        <div className="mt-4">{children}</div>
      </div>
    </div>
  );
}
