import type { TicketType } from "@/types";
import { TicketTable } from "@/components/TicketTable";
import { Actions } from "@/components/Action";
import { useTickets } from "@/hooks/use-tickets";
import { useEffect } from "react";
import { APP_MIN_HEIGHT, EMPTY_TICKET } from "@/data/constants";

const TicketsPage = () => {
  const { origTickets, openedActionTicket, setOpenedActionTicket } = useTickets();

  // update opened actions ticket
  useEffect(() => {
    if (!openedActionTicket?.id) return;

    let newOpenedActionTicket: TicketType | undefined;
    // deleted ticket
    if (!origTickets.some((ticket) => ticket.id === openedActionTicket.id)) {
      newOpenedActionTicket = EMPTY_TICKET;
      // edited ticket
    } else {
      newOpenedActionTicket = origTickets.find((ticket) => ticket.id === openedActionTicket.id);
    }
    setOpenedActionTicket(newOpenedActionTicket);
  }, [origTickets, openedActionTicket?.id, setOpenedActionTicket]);

  const handleActions = (ticket: TicketType) => {
    if (ticket.id !== openedActionTicket?.id) {
      setOpenedActionTicket(ticket);
    } else {
      setOpenedActionTicket(undefined);
    }
  }

  const handleActionsExit = () => {
    if (setOpenedActionTicket) setOpenedActionTicket(undefined);
  };

  return (
    <main className={`h-[100vh] grid grid-cols-1`} style={{ minHeight: APP_MIN_HEIGHT }}>
      <div className={`flex flex-row min-h-0`}>
        <section className={`overflow-auto p-4 flex-1 ${openedActionTicket && "hidden xl:block"}`}>
          <TicketTable edit={true} variant="combo" onActionClick={handleActions} />
        </section>

        <section className={`flex-1 min-h-0 min-w-0 xl:max-w-md ${openedActionTicket ? "block" : "hidden"}`}>
          <Actions variant="full" onActionsExitClick={handleActionsExit} />
        </section>
      </div>
    </main>
  );
};

export default TicketsPage;
