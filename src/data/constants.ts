import type { TicketType } from "@/types";

const APP_MIN_HEIGHT = "650px";
const APP_MAX_HEIGHT = "100vh";

const APP_MIN_WIDTH = "404px";
const APP_MAX_WIDTH = "100vw";

const MAIN_MIN_WIDTH = "404px";

const EMPTY_TICKET: TicketType = {
    id: "",
    title: "",
    status: "",
    category: "",
    description: "",
    files: [],
    createdAt: "",
    updatedAt: "",
    assignedTo: {
        id: "",
        name: "",
        role: "",
        imagePath: "",
    },
};

export { APP_MIN_HEIGHT, APP_MAX_HEIGHT, APP_MIN_WIDTH, APP_MAX_WIDTH, MAIN_MIN_WIDTH, EMPTY_TICKET };
