import { forwardRef, type SelectHTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  error?: boolean;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <select
        ref={ref}
        className={cn(
          "h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-900 shadow-sm outline-none transition focus:border-blue-500 focus:ring-1 focus:ring-blue-500",
          error && "border-red-400 focus:border-red-500 focus:ring-red-500",
          className
        )}
        {...props}
      />
    );
  }
);

Select.displayName = "Select";
