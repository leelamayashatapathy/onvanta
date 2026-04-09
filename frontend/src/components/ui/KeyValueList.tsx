import type { ReactNode } from "react";

interface KeyValueListProps {
  items: Array<{ label: string; value: ReactNode }>;
}

export function KeyValueList({ items }: KeyValueListProps) {
  return (
    <dl className="grid gap-3">
      {items.map((item) => (
        <div key={item.label} className="flex items-start justify-between gap-3">
          <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            {item.label}
          </dt>
          <dd className="text-sm font-medium text-slate-900 text-right">{item.value}</dd>
        </div>
      ))}
    </dl>
  );
}
