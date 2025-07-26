type FileType = {
    name: string;
    size: number;
    type: string;
    uploadedAt: string;
};

type TicketType = {
    id: string;
    title: string;
    status: "Open" | "In progress" | "Resolved" | "Closed" | "";
    category: "Hardware" | "Software" | "Network" | "Access" | "Support" | "";
    description: string;
    files: FileType[];
    createdAt: string;
    updatedAt: string;
    assignedTo: {
        id: string;
        name: string;
        role: "client" | "support" | "admin" | "";
        imagePath: string;
    };
};

type StatusSummaryType = {
    status: "Open" | "In progress" | "Resolved" | "Closed" | "";
    count: number;
};

type ChatType = {
    source: "you" | "other" | "";
    date: string;
    message: string;
};

type ActionTabType = "details" | "chat" | "filter" | "edit" | "others";

export { type TicketType, type StatusSummaryType, type ChatType, type ActionTabType, type FileType };
