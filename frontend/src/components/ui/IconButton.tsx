import type { ButtonHTMLAttributes } from "react";
import { cn } from "../../lib/utils/cn";

interface IconButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "ghost" | "subtle";
}

export function IconButton({
  className,
  variant = "ghost",
  ...props
}: IconButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex h-9 w-9 items-center justify-center rounded-xl transition focus-ring",
        variant === "ghost" && "hover:bg-slate-100",
        variant === "subtle" && "bg-slate-100 hover:bg-slate-200",
        className
      )}
      {...props}
    />
  );
}
