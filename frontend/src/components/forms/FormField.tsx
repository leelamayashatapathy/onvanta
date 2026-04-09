import type { HTMLAttributes, ReactNode } from "react";

interface FormFieldProps extends HTMLAttributes<HTMLDivElement> {
  label: string;
  error?: string;
  helper?: string;
  children: ReactNode;
}

export function FormField({ label, error, helper, children, ...props }: FormFieldProps) {
  return (
    <div className="space-y-2" {...props}>
      <label className="text-sm font-medium text-slate-700">{label}</label>
      {children}
      {helper ? <p className="text-xs text-slate-500">{helper}</p> : null}
      {error ? <p className="text-xs text-red-600">{error}</p> : null}
    </div>
  );
}
