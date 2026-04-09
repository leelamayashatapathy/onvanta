import { format } from "date-fns";

export function formatDate(value: string, pattern = "MMM d, yyyy") {
  try {
    return format(new Date(value), pattern);
  } catch {
    return value;
  }
}

export function formatShortDate(value: string) {
  return formatDate(value, "MMM d");
}
