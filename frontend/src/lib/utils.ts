import type { TicketType } from "@/types";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

function selectStatusBGColor(status: TicketType["status"]) {
    switch (status) {
        case "Open":
            return "bg-gray-500";
        case "In progress":
            return "bg-blue-500";
        case "Resolved":
            return "bg-green-500";
        case "Closed":
            return "bg-yellow-500";
        default:
            return "";
    }
}

function selectRoleBGColor(assignedTo: TicketType["assignedTo"]) {
    switch (assignedTo?.role) {
        case "admin":
            return "bg-purple-500";
        case "support":
            return "bg-blue-500";
        case "client":
            return "bg-green-500";
        default:
            return "";
    }
}

export { cn, selectStatusBGColor, selectRoleBGColor };
