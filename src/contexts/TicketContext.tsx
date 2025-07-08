import React, { createContext, useContext, useState, type ReactNode } from "react";
import type { TicketType } from "@/types";

const populateTicketArr = (arr: TicketType[], count: number) => {
    const populatedArr: TicketType[] = [];
    for (let i = 0; i < count; i++) {
        arr.forEach((t) => populatedArr.push({ ...t }));
    }
    populatedArr.forEach((ticket, index) => (ticket.id = `T-${index}`));
    return populatedArr;
};

type TicketContextType = {
    origTickets: TicketType[];
    setOrigTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
    copyTickets: TicketType[];
    setCopyTickets: React.Dispatch<React.SetStateAction<TicketType[]>>;
};

const TicketContext = createContext<TicketContextType | undefined>(undefined);

const TicketProvider = ({ children }: { children: ReactNode }) => {
    const defaultTickets: TicketType[] = populateTicketArr(
        [
            {
                id: "",
                title: "my 1st ticket mf",
                status: "Unassigned",
                created_at: "2024-10-09",
                updated_at: "2024-10-09",
                assigned_to: "@bentot",
            },
            {
                id: "",
                title: "my 2nd ticket mf",
                status: "In Progress",
                created_at: "2024-10-09",
                updated_at: "2024-10-09",
                assigned_to: "@juantot",
            },
            {
                id: "",
                title: "my 3rd ticket mf",
                status: "Resolved",
                created_at: "2024-10-09",
                updated_at: "2024-10-09",
                assigned_to: "@gwentot",
            },
            {
                id: "",
                title: "my 4th ticket mf",
                status: "Closed",
                created_at: "2024-10-09",
                updated_at: "2024-10-09",
                assigned_to: "@kwintot",
            },
        ],
        20
    );
    const [origTickets, setOrigTickets] = useState<TicketType[]>([...defaultTickets]);
    const [copyTickets, setCopyTickets] = useState<TicketType[]>([...defaultTickets]);
    return (
        <TicketContext.Provider value={{ origTickets, setOrigTickets, copyTickets, setCopyTickets }}>
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
