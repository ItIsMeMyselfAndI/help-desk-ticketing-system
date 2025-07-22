import type { TicketType } from "@/types";
import { TicketTable } from "@/components/TicketTable";
import { Actions } from "@/components/Action";
import { useTicketContext } from "@/contexts/TicketContext";
import { useEffect } from "react";

const TicketsPage = () => {
    const { origTickets, openedActionTicket, setOpenedActionTicket } = useTicketContext();

    useEffect(() => {
        if (!openedActionTicket?.id) return;
        const newOpenedActionTicket = origTickets.find((ticket) => ticket.id === openedActionTicket.id);
        setOpenedActionTicket(newOpenedActionTicket);
    }, [origTickets, openedActionTicket?.id, setOpenedActionTicket]);

    const handleActions = (ticket: TicketType) => {
        if (ticket.id !== openedActionTicket?.id) {
            setOpenedActionTicket(ticket);
        } else {
            setOpenedActionTicket(undefined);
        }
    };

    const handleActionsExit = () => {
        if (setOpenedActionTicket) setOpenedActionTicket(undefined);
    };

    return (
        <div className="h-[100vh] grid grid-cols-15 gap-4">
            <div className={`${openedActionTicket ? "col-span-10 py-4 pl-4" : "col-span-15 p-4"} overflow-auto`}>
                <TicketTable edit={true} variant="combo" onActionClick={handleActions} />
            </div>

            <div className={`${openedActionTicket ? "col-span-5" : "hidden"}`}>
                <Actions onActionsExitClick={handleActionsExit} />
            </div>
        </div>
    );
};

export default TicketsPage;
