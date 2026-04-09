import { formatShortDate } from "../../lib/formatters/date";

interface ActivityFeedItemProps {
  title: string;
  description: string;
  timestamp: string;
}

export function ActivityFeedItem({ title, description, timestamp }: ActivityFeedItemProps) {
  return (
    <div className="space-y-1 rounded-xl border border-slate-200 bg-white px-4 py-3">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-slate-900">{title}</p>
        <span className="text-xs text-slate-500">{formatShortDate(timestamp)}</span>
      </div>
      <p className="text-sm text-slate-600">{description}</p>
    </div>
  );
}
