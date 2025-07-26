import { TicketContext } from "@/contexts/TicketContext";
import { useContext } from "react";

const useTickets = () => {
    const context = useContext(TicketContext);
    if (!context) {
        throw new Error("useTickets must be used within a TicketProvider");
    }
    return context;
};

export { useTickets };
