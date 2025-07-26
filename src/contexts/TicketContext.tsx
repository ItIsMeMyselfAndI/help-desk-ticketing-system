import React, { createContext, useRef, useState, type ReactNode, type RefObject } from "react";
import type { TicketType } from "@/types";
import ticketsSample from "@/data/tickets.sample.json";

type TicketContextType = {
    // states
    origTickets: TicketType[];
    prevModifiedTickets: RefObject<TicketType[]>;
    displayTickets: TicketType[];
    selectedTicketIDs: Set<string>;
    isAllSelected: boolean;
    openedActionTicket: TicketType | undefined;
    // setters
    setOrigTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
    setDisplayTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
    setSelectedTicketIDs: React.Dispatch<React.SetStateAction<Set<string>>>;
    setIsAllSelected: React.Dispatch<React.SetStateAction<boolean>>;
    setOpenedActionTicket: React.Dispatch<React.SetStateAction<TicketType | undefined>>;
};

const TicketContext = createContext<TicketContextType | undefined>(undefined);

const TicketProvider = ({ children }: { children: ReactNode }) => {
    const [origTickets, setOrigTickets] = useState<TicketType[]>(ticketsSample as TicketType[]);
    const prevModifiedTickets = useRef<TicketType[]>([]);
    const [displayTickets, setDisplayTickets] = useState<TicketType[]>(ticketsSample as TicketType[]);
    const [selectedTicketIDs, setSelectedTicketIDs] = useState<Set<string>>(new Set());
    const [isAllSelected, setIsAllSelected] = useState<boolean>(false);
    const [openedActionTicket, setOpenedActionTicket] = useState<TicketType | undefined>(undefined);
    return (
        <TicketContext.Provider
            value={{
                // states
                origTickets,
                prevModifiedTickets,
                displayTickets,
                selectedTicketIDs,
                isAllSelected,
                openedActionTicket,
                // setters
                setOrigTickets,
                setDisplayTickets,
                setSelectedTicketIDs,
                setIsAllSelected,
                setOpenedActionTicket,
            }}
        >
            {children}
        </TicketContext.Provider>
    );
};

export { TicketProvider, TicketContext };
