import { useState } from "react";
import type { TicketType } from "@/types";
import { TicketTable } from "@/components/TicketTable";
import { Action } from "@/components/Action";

const TicketsPage = () => {
    const [openedTicket, setOpenedTicket] = useState<TicketType | undefined>(undefined);

    const handleAction = (ticket: TicketType) => {
        if (ticket.id !== openedTicket?.id) {
            setOpenedTicket(ticket);
        } else {
            setOpenedTicket(undefined);
        }
    };

    const handleActionExit = () => {
        if (setOpenedTicket) setOpenedTicket(undefined);
    };

    return (
        <div className="h-[100vh] grid grid-cols-15 gap-4">
            <div className={`${openedTicket ? "col-span-10 py-4 pl-4" : "col-span-15 p-4"} overflow-auto`}>
                <TicketTable edit={true} variant="combo" onActionClick={handleAction} />
            </div>

            <div className={`${openedTicket ? "col-span-5" : "hidden"}`}>
                <Action openedTicket={openedTicket} onActionExitClick={handleActionExit} />
            </div>
        </div>
    );
};

export default TicketsPage;
