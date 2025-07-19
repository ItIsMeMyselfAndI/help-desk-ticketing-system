import React, { createContext, useContext, useState, type ReactNode } from "react";
import type { TicketType } from "@/types";
import ticketsSample from "@/data/tickets.sample.json";

type TicketContextType = {
    // states
    origTickets: TicketType[];
    copyTickets: TicketType[];
    displayTickets: TicketType[];
    selectedTicketIDs: Set<string>;
    isAllSelected: boolean;
    // setters
    setOrigTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
    setCopyTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
    setDisplayTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
    setSelectedTicketIDs: React.Dispatch<React.SetStateAction<Set<string>>>;
    setIsAllSelected: React.Dispatch<React.SetStateAction<boolean>>;
};

const TicketContext = createContext<TicketContextType | undefined>(undefined);

const TicketProvider = ({ children }: { children: ReactNode }) => {
    const [origTickets, setOrigTickets] = useState<TicketType[]>(ticketsSample as TicketType[]);
    const [copyTickets, setCopyTickets] = useState<TicketType[]>(ticketsSample as TicketType[]);
    const [displayTickets, setDisplayTickets] = useState<TicketType[]>(ticketsSample as TicketType[]);
    const [selectedTicketIDs, setSelectedTicketIDs] = useState<Set<string>>(new Set());
    const [isAllSelected, setIsAllSelected] = useState<boolean>(false);
    return (
        <TicketContext.Provider
            value={{
                // states
                origTickets,
                copyTickets,
                displayTickets,
                selectedTicketIDs,
                isAllSelected,
                // setters
                setOrigTickets,
                setCopyTickets,
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
