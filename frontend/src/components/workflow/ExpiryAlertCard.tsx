import { Badge } from "../ui/Badge";

interface ExpiryAlertCardProps {
  vendor: string;
  document: string;
  daysRemaining: number;
  owner: string;
}

export function ExpiryAlertCard({ vendor, document, daysRemaining, owner }: ExpiryAlertCardProps) {
  const tone = daysRemaining <= 0 ? "error" : daysRemaining <= 7 ? "warning" : "info";
  const label = daysRemaining <= 0 ? "Overdue" : `${daysRemaining} days`;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-slate-900">{vendor}</p>
        <Badge tone={tone}>{label}</Badge>
      </div>
      <p className="text-xs text-slate-500">{document}</p>
      <p className="mt-2 text-xs text-slate-500">Owner: {owner}</p>
    </div>
  );
}
