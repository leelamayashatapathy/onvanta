import { Badge } from "../ui/Badge";
import type { VendorDocument } from "../../types";
import { formatDate } from "../../lib/formatters/date";

interface DocumentCardProps {
  document: VendorDocument;
}

const statusTone: Record<VendorDocument["status"], "neutral" | "success" | "warning" | "error" | "info"> = {
  active: "success",
  expired: "error",
  rejected: "error",
  pending: "warning",
  under_review: "warning",
};

export function DocumentCard({ document }: DocumentCardProps) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold text-slate-900">Document {document.document_type}</p>
          <p className="text-xs text-slate-500">{document.original_name}</p>
        </div>
        <Badge tone={statusTone[document.status]}>{document.status}</Badge>
      </div>
      <div className="mt-3 grid gap-2 text-xs text-slate-500 md:grid-cols-2">
        <span>Issue: {document.issue_date ? formatDate(document.issue_date) : "N/A"}</span>
        <span>Expiry: {document.expiry_date ? formatDate(document.expiry_date) : "N/A"}</span>
        <span>Version: v{document.version}</span>
        <span>Uploaded by: {document.uploaded_by ?? "—"}</span>
      </div>
      {document.rejection_reason ? (
        <div className="mt-3 rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
          Rejected: {document.rejection_reason}
        </div>
      ) : null}
    </div>
  );
}
