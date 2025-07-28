type FileType = { name: string; size: number; type: string; uploadedAt: string };

type TicketType = {
    id: string;
    title: string;
    status: "Open" | "In progress" | "Resolved" | "Closed" | "";
    category: "Hardware" | "Software" | "Network" | "Access" | "Support" | "";
    description: string;
    files: File[] | FileType[];
    createdAt: string;
    updatedAt: string;
    assignedTo: null | {
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

type FormTabType = "form" | "upload";

export type { TicketType, StatusSummaryType, ChatType, ActionTabType, FormTabType, FileType };
