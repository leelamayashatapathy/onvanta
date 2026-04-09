import { Card } from "./Card";

interface MetricCardProps {
  label: string;
  value: string;
  helper?: string;
}

export function MetricCard({ label, value, helper }: MetricCardProps) {
  return (
    <Card className="space-y-2">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</p>
      <p className="text-3xl font-semibold text-slate-900">{value}</p>
      {helper ? <p className="text-sm text-slate-600">{helper}</p> : null}
    </Card>
  );
}
