import React, { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardTitle } from "@/components/ui/card";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { useTicketContext } from "@/contexts/TicketContext";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Check, Trash2Icon, Undo2, X } from "lucide-react";
import type { TicketType } from "@/types";

type StatusChangeSelectionProp = {
    selectedStatus: string;
    setSelectedStatus: React.Dispatch<React.SetStateAction<string>>;
};

const StatusChangeSelection = ({ selectedStatus, setSelectedStatus }: StatusChangeSelectionProp) => {
    const defaultItem = "None";

    const handleSelectionChange = (value: string) => {
        setSelectedStatus(value);
    };

    const statuses = ["Re-open", "Close"];

    return (
        <Select value={selectedStatus} onValueChange={handleSelectionChange}>
            <SelectTrigger
                className={`w-full text-foreground data-[size=default]:h-full bg-muted hover:bg-accent ${
                    selectedStatus === defaultItem && "text-muted-foreground"
                }`}
            >
                <SelectValue placeholder={defaultItem} />
            </SelectTrigger>

            <SelectContent>
                <SelectGroup>
                    <SelectLabel className="text-lg text-foreground/50">Select status</SelectLabel>
                    <SelectItem
                        className="text-muted-foreground focus:bg-accent focus:text-muted-foreground"
                        value={defaultItem}
                    >
                        None
                    </SelectItem>
                    {statuses.map((val: string) => (
                        <SelectItem key={val.toLowerCase()} className="focus:bg-primary" value={val}>
                            {val}
                        </SelectItem>
                    ))}
                </SelectGroup>
            </SelectContent>
        </Select>
    );
};

type QuickEditProps = {
    padding?: string;
    hasBorder?: boolean;
    bgColor?: string;
};

const QuickEdit = ({ padding, hasBorder = true, bgColor = "bg-card" }: QuickEditProps) => {
    const {
        origTickets,
        displayTickets,
        setOrigTickets,
        recentModifiedTickets,
        setRecentModifiedTickets,
        selectedTicketIDs,
        setSelectedTicketIDs,
        isAllSelected,
        setIsAllSelected,
    } = useTicketContext();
    const [selectedStatus, setSelectedStatus] = useState<string>("None");

    const toggleSelectAll = () => {
        if (isAllSelected) {
            setSelectedTicketIDs(new Set());
            setIsAllSelected(false);
        } else {
            setSelectedTicketIDs(new Set(displayTickets.map((ticket) => ticket.id)));
            setIsAllSelected(true);
        }
    };

    const handleUpdateStatus = () => {
        if (selectedStatus === "None" || selectedTicketIDs.size === 0) return;
        setRecentModifiedTickets([...origTickets].filter((ticket) => selectedTicketIDs.has(ticket.id)));

        setOrigTickets((prev) => {
            const updatedTickets = prev.map((ticket) => {
                if (!selectedTicketIDs.has(ticket.id)) return ticket;
                else if (selectedStatus === "Re-open") return { ...ticket, status: "Open" as TicketType["status"] };
                else if (selectedStatus === "Close") return { ...ticket, status: "Closed" as TicketType["status"] };
                else {
                    return ticket;
                }
            });
            return updatedTickets;
        });
    };

    const handleDeleteTickets = () => {
        if (selectedTicketIDs.size === 0) return;
        setRecentModifiedTickets([...origTickets].filter((ticket) => selectedTicketIDs.has(ticket.id)));

        setOrigTickets((prev) => {
            const newTickets = prev.filter((ticket) => !selectedTicketIDs.has(ticket.id));
            return newTickets;
        });
    };

    const handleUndoChanges = () => {
        const currTicketIDs = origTickets.map((ticket) => ticket.id);
        const undoneTickets = [...origTickets];
        recentModifiedTickets.forEach((ticket) => {
            // recover deleted tickets
            if (!currTicketIDs.includes(ticket.id)) {
                undoneTickets.push(ticket);
            }
            // undo last changes
            else {
                const i = undoneTickets.findIndex((undoneTicket) => undoneTicket.id === ticket.id);
                undoneTickets[i] = ticket;
            }
        });
        const sortedTickets = undoneTickets.sort((a, b) => a.id.localeCompare(b.id));
        setOrigTickets(sortedTickets);
    };

    useEffect(() => {
        console.log(recentModifiedTickets);
    }, [recentModifiedTickets]);

    return (
        <Card
            className={`px-6 gap-0 h-full flex flex-col justify-evenly ${bgColor}
                ${!hasBorder && "border-none"} ${padding || ""}`}
        >
            <CardTitle className="flex justify-between text-2xl text-primary">
                <span>Quick Edit</span>
            </CardTitle>

            <CardContent className="flex flex-col justify-evenly gap-4">
                <section className="flex justify-between">
                    <div className="flex items-center gap-2">
                        <Checkbox className="size-5 bg-muted" onClick={toggleSelectAll} />
                        <CardDescription className="text-lg font-medium">Select all tickets</CardDescription>
                    </div>

                    <Button
                        onClick={handleUndoChanges}
                        className="bg-primary hover:bg-primary hover:ring-2 hover:ring-primary active:bg-primary/50 active:ring-primary/50"
                    >
                        <span>undo</span>
                        <Undo2 className="scale-150 m-1.5" />
                    </Button>
                </section>

                <section className="flex-1 flex flex-col gap-2">
                    <CardDescription className="text-lg">Change status</CardDescription>
                    <StatusChangeSelection selectedStatus={selectedStatus} setSelectedStatus={setSelectedStatus} />
                </section>

                <section className="flex-1 grid grid-cols-2 gap-2">
                    <Button
                        onClick={handleUpdateStatus}
                        className="h-full bg-green-500 hover:bg-green-500 hover:ring-2 hover:ring-green-500 active:bg-green-600 active:ring-green-600"
                    >
                        <Check className="scale-150 m-1.5 text-foreground" />
                    </Button>
                    <Button
                        onClick={() => {
                            setSelectedStatus("None");
                        }}
                        className="h-full bg-yellow-500 hover:bg-yellow-500 hover:ring-2 hover:ring-yellow-500 active:bg-yellow-600 active:ring-yellow-600"
                    >
                        <X className="scale-150 m-1.5 text-foreground" />
                    </Button>
                </section>

                <section className="flex flex-col flex-1">
                    <CardDescription className="text-lg">Delete ticket(s)</CardDescription>
                    <Button
                        onClick={handleDeleteTickets}
                        className="flex-1 bg-red-500 hover:bg-red-500 hover:ring-2 hover:ring-red-500 active:bg-red-600 active:ring-red-600"
                    >
                        <Trash2Icon className="scale-150 m-1.5" />
                    </Button>
                </section>
            </CardContent>
        </Card>
    );
};

export { QuickEdit };
