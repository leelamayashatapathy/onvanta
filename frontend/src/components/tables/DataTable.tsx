import type { ReactNode } from "react";
import { cn } from "../../lib/utils/cn";

interface DataTableProps {
  columns: string[];
  rows: ReactNode[][];
  emptyState?: ReactNode;
}

export function DataTable({ columns, rows, emptyState }: DataTableProps) {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
      <table className="min-w-full border-separate border-spacing-0">
        <thead className="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500">
          <tr>
            {columns.map((col) => (
              <th key={col} className="px-4 py-3 text-left">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="text-sm text-slate-700">
          {rows.length === 0 ? (
            <tr>
              <td className="px-4 py-6" colSpan={columns.length}>
                {emptyState ?? (
                  <div className="text-sm text-slate-500">No records available.</div>
                )}
              </td>
            </tr>
          ) : (
            rows.map((row, rowIndex) => (
              <tr
                key={`row-${rowIndex}`}
                className={cn(rowIndex % 2 === 0 ? "bg-white" : "bg-slate-50")}
              >
                {row.map((cell, cellIndex) => (
                  <td key={`cell-${rowIndex}-${cellIndex}`} className="px-4 py-3">
                    {cell}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
