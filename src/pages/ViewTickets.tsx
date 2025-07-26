import type { TicketType } from "@/types";
import { TicketTable } from "@/components/TicketTable";
import { Actions } from "@/components/Action";
import { useTicketContext } from "@/contexts/TicketContext";
import { useEffect } from "react";
import { APP_MIN_HEIGHT } from "@/data/constants";

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
        <div className={`h-[100vh] grid grid-cols-1 min-h-${APP_MIN_HEIGHT}`}>
            <div className={`min-h-[${APP_MIN_HEIGHT}] flex flex-row`}>
                <div className={`overflow-auto p-4 flex-1 ${openedActionTicket && "hidden xl:block"}`}>
                    <TicketTable edit={true} variant="combo" onActionClick={handleActions} />
                </div>

                <div className={`flex-1 min-h-0 min-w-md xl:max-w-md ${openedActionTicket ? "block" : "hidden"}`}>
                    <Actions variant="full" onActionsExitClick={handleActionsExit} />
                </div>
            </div>
        </div>
    );
};

export default TicketsPage;
