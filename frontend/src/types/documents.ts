export type DocumentStatus =
  | "active"
  | "expired"
  | "rejected"
  | "pending"
  | "under_review";

export interface VendorDocument {
  id: string;
  vendor: string;
  document_type: string;
  file: string;
  file_path: string;
  original_name: string;
  mime_type: string;
  file_size: number;
  checksum: string;
  version: number;
  issue_date: string | null;
  expiry_date: string | null;
  status: DocumentStatus;
  verification_status: string;
  verified_by: string | null;
  verified_at: string | null;
  rejection_reason: string | null;
  supersedes_document: string | null;
  uploaded_by: string | null;
  uploaded_at: string;
  created_at: string;
  updated_at: string;
}

export interface ExpiryItem {
  document_id: string;
  vendor_id: string;
  vendor_name: string;
  document_type: string;
  expiry_date: string;
}
