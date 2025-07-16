type TicketType = {
  id: string;
  title: string;
  status: "Unassigned" | "In progress" | "Resolved" | "Closed";
  created_at: string;
  updated_at: string;
  assigned_to: string;
};

type StatusSummaryType = {
  status: string;
  count: number;
};
export { type TicketType, type StatusSummaryType };
