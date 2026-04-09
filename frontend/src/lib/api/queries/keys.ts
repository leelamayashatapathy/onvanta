export const QUERY_KEYS = {
  session: ["session"] as const,
  dashboard: ["dashboard"] as const,
  vendors: ["vendors"] as const,
  vendor: (id: string) => ["vendors", id] as const,
  onboarding: ["onboarding"] as const,
  documents: ["documents"] as const,
  approvals: ["approvals"] as const,
  expiries: ["expiries"] as const,
  tasks: ["tasks"] as const,
  audit: ["audit"] as const,
  settings: ["settings"] as const,
  members: ["members"] as const,
};
