import type { ReactNode } from "react";

interface PageContainerProps {
  title?: string;
  description?: string;
  action?: ReactNode;
  children: ReactNode;
}

export function PageContainer({ title, description, action, children }: PageContainerProps) {
  return (
    <div className="space-y-6">
      {title ? (
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900">{title}</h1>
            {description ? (
              <p className="mt-1 text-sm text-slate-600">{description}</p>
            ) : null}
          </div>
          {action ? <div>{action}</div> : null}
        </div>
      ) : null}
      {children}
    </div>
  );
}
