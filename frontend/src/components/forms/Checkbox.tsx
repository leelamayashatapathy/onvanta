import type { InputHTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

interface CheckboxProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

export function Checkbox({ label, className, ...props }: CheckboxProps) {
  return (
    <label className="flex items-center gap-2 text-sm text-slate-700">
      <input
        type="checkbox"
        className={cn("h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500", className)}
        {...props}
      />
      {label}
    </label>
  );
}
