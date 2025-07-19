type TicketType = {
    id: string;
    title: string;
    status: "Open" | "In progress" | "Resolved" | "Closed";
    created_at: string;
    updated_at: string;
    assigned_to: string;
};

type StatusSummaryType = {
    status: "Open" | "In progress" | "Resolved" | "Closed";
    count: number;
};
export { type TicketType, type StatusSummaryType };
