import type { InputHTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

interface FileUploadProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function FileUpload({ label = "Upload file", className, ...props }: FileUploadProps) {
  return (
    <label className="flex cursor-pointer items-center justify-between rounded-2xl border border-dashed border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-600">
      <span>{label}</span>
      <input
        type="file"
        className={cn("hidden", className)}
        {...props}
      />
      <span className="text-xs font-semibold text-blue-600">Choose file</span>
    </label>
  );
}
