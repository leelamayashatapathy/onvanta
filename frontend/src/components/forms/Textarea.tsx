import { forwardRef, type TextareaHTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: boolean;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <textarea
        ref={ref}
        className={cn(
          "min-h-[110px] w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none transition focus:border-blue-500 focus:ring-1 focus:ring-blue-500",
          error && "border-red-400 focus:border-red-500 focus:ring-red-500",
          className
        )}
        {...props}
      />
    );
  }
);

Textarea.displayName = "Textarea";
