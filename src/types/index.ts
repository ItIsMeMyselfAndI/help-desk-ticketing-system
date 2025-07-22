type TicketType = {
    id: string;
    title: string;
    status: "Open" | "In progress" | "Resolved" | "Closed";
    description: string;
    created_at: string;
    updated_at: string;
    assigned_to: {
        name: string;
        role: "client" | "support" | "admin";
        imagePath: string;
    };
};

type StatusSummaryType = {
    status: "Open" | "In progress" | "Resolved" | "Closed";
    count: number;
};
export { type TicketType, type StatusSummaryType };
