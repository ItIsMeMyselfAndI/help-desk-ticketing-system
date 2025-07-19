import React, { createContext, useContext, useState, type ReactNode } from "react";
import type { TicketType } from "@/types";
import ticketsSample from "@/data/tickets.sample.json";

type TicketContextType = {
    // states
    origTickets: TicketType[];
    recentModifiedTickets: TicketType[];
    displayTickets: TicketType[];
    selectedTicketIDs: Set<string>;
    isAllSelected: boolean;
    // setters
    setOrigTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
    setRecentModifiedTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
    setDisplayTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
    setSelectedTicketIDs: React.Dispatch<React.SetStateAction<Set<string>>>;
    setIsAllSelected: React.Dispatch<React.SetStateAction<boolean>>;
};

const TicketContext = createContext<TicketContextType | undefined>(undefined);

const TicketProvider = ({ children }: { children: ReactNode }) => {
    const [origTickets, setOrigTickets] = useState<TicketType[]>(ticketsSample as TicketType[]);
    const [recentModifiedTickets, setRecentModifiedTickets] = useState<TicketType[]>([]);
    const [displayTickets, setDisplayTickets] = useState<TicketType[]>(ticketsSample as TicketType[]);
    const [selectedTicketIDs, setSelectedTicketIDs] = useState<Set<string>>(new Set());
    const [isAllSelected, setIsAllSelected] = useState<boolean>(false);
    return (
        <TicketContext.Provider
            value={{
                // states
                origTickets,
                recentModifiedTickets,
                displayTickets,
                selectedTicketIDs,
                isAllSelected,
                // setters
                setOrigTickets,
                setRecentModifiedTickets,
                setDisplayTickets,
                setSelectedTicketIDs,
                setIsAllSelected,
            }}
        >
            {children}
        </TicketContext.Provider>
    );
};

const useTicketContext = () => {
    const context = useContext(TicketContext);
    if (!context) {
        throw new Error("useTicketContext must be used within a TicketProvider");
    }
    return context;
};

export { TicketProvider, useTicketContext };
