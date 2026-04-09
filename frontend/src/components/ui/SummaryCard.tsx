import { Card } from "./Card";

interface SummaryCardProps {
  title: string;
  description?: string;
  value?: string;
}

export function SummaryCard({ title, description, value }: SummaryCardProps) {
  return (
    <Card className="space-y-2">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-slate-900">{title}</p>
        {value ? <span className="text-xs font-semibold text-slate-500">{value}</span> : null}
      </div>
      {description ? <p className="text-sm text-slate-600">{description}</p> : null}
    </Card>
  );
}
