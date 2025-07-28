import type { TicketType } from "@/types";
import { getYearOptions } from "./filterOptions";

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
    assignedTo: null,
};

const STATUSES = ["Open", "In progress", "Resolved", "Closed"];
const CATEGORIES = ["Hardware", "Software", "Access", "Network", "Support"];
const YEARS = getYearOptions();
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const ASSIGNMENT_TO = ["@bentot", "@juantot", "@gwentot", "@kwintot"];

export {
    // ui
    APP_MIN_HEIGHT,
    APP_MAX_HEIGHT,
    APP_MIN_WIDTH,
    APP_MAX_WIDTH,
    MAIN_MIN_WIDTH,
    // data
    EMPTY_TICKET,
    STATUSES,
    CATEGORIES,
    YEARS,
    MONTHS,
    ASSIGNMENT_TO,
};
