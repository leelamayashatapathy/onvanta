import type { AuditEvent } from "../../types";
import { formatDate } from "../../lib/formatters/date";

interface AuditEventCardProps {
  event: AuditEvent;
}

export function AuditEventCard({ event }: AuditEventCardProps) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-slate-900">{event.action}</p>
        <span className="text-xs text-slate-500">{formatDate(event.created_at)}</span>
      </div>
      <p className="text-xs text-slate-500">
        {event.entity_type} · {event.entity_id}
      </p>
      <p className="mt-2 text-xs text-slate-500">Actor: {event.actor_user ?? "System"}</p>
    </div>
  );
}
