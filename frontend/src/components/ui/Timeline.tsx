import type { ReactNode } from "react";

interface TimelineItem {
  id: string;
  title: string;
  meta: string;
  content?: ReactNode;
}

interface TimelineProps {
  items: TimelineItem[];
}

export function Timeline({ items }: TimelineProps) {
  return (
    <div className="space-y-4">
      {items.map((item) => (
        <div key={item.id} className="flex gap-4">
          <div className="mt-1 h-2 w-2 rounded-full bg-blue-500" />
          <div className="flex-1 space-y-1">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-900">{item.title}</p>
              <span className="text-xs text-slate-500">{item.meta}</span>
            </div>
            {item.content ? <div className="text-sm text-slate-600">{item.content}</div> : null}
          </div>
        </div>
      ))}
    </div>
  );
}
