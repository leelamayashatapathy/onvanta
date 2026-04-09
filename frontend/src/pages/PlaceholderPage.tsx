import { PageContainer } from "../components/layout/PageContainer";
import { Card } from "../components/ui/Card";

interface PlaceholderPageProps {
  title: string;
  description: string;
}

export function PlaceholderPage({ title, description }: PlaceholderPageProps) {
  return (
    <PageContainer title={title} description="This workspace area is being built.">
      <Card className="space-y-2">
        <p className="text-sm font-semibold text-slate-900">Phase 1 placeholder</p>
        <p className="text-sm text-slate-600">{description}</p>
      </Card>
    </PageContainer>
  );
}
