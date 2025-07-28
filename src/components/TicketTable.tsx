import { useTickets } from "@/hooks/use-tickets";
import type { TicketType } from "@/types";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Checkbox } from "@/components/ui/checkbox";
import { selectRoleBGColor, selectStatusBGColor } from "@/lib/utils";
import { Button } from "./ui/button";
import { Ellipsis } from "lucide-react";

type TicketTableProps = {
    edit?: true | false;
    variant?: "default" | "message" | "full" | "combo";
    onActionClick?: (ticket: TicketType) => void;
};

const TicketTable = ({ edit = false, variant = "default", onActionClick }: TicketTableProps) => {
    const { displayTickets, openedActionTicket, setOpenedActionTicket, selectedTicketIDs, setSelectedTicketIDs } =
        useTickets();

    const showFullTable = variant === "full" || variant === "combo";
    const showActionColumn = variant === "message" || variant === "combo";

    const toggleRowSelection = (id: string) => {
        setSelectedTicketIDs((prev) => {
            const selectedTicketIDsCopy = new Set(prev);
            if (selectedTicketIDsCopy.has(id)) {
                selectedTicketIDsCopy.delete(id);
            } else {
                selectedTicketIDsCopy.add(id);
            }
            return selectedTicketIDsCopy;
        });
    };

    const handleAction = (e: React.MouseEvent, ticket: TicketType) => {
        e.stopPropagation();
        if (onActionClick) onActionClick(ticket);
        if (openedActionTicket?.id !== ticket.id) {
            setOpenedActionTicket(ticket);
        } else {
            setOpenedActionTicket(undefined);
        }
    };

    return (
        <div className="h-full flex flex-col gap-2">
            <Table className="bg-card w-full text-sm lg:text-lg">
                <TableHeader className="bg-muted h-15 sticky top-0 z-1">
                    <TableRow key="header" className="text-lg lg:text-xl">
                        {edit && <TableHead className="text-primary pl-5">Edit</TableHead>}
                        <TableHead className={`text-primary ${!edit && "pl-5"}`}>Ticket</TableHead>
                        <TableHead className="text-primary">Title</TableHead>
                        <TableHead className="text-primary">Status</TableHead>
                        {showFullTable && <TableHead className="text-primary text-left">Category</TableHead>}
                        <TableHead className="text-primary text-right">Submitted At</TableHead>
                        {showFullTable && <TableHead className="text-primary text-right">Updated At</TableHead>}
                        <TableHead className="text-primary text-right pr-5">Assigned To</TableHead>
                        {showActionColumn && <TableHead className="text-primary text-right pr-5">Actions</TableHead>}
                    </TableRow>
                </TableHeader>

                <TableBody>
                    {displayTickets.map((ticket) => (
                        <TableRow key={ticket.id} onClick={edit ? () => toggleRowSelection(ticket.id) : undefined}>
                            {edit && (
                                <TableCell className="pl-5">
                                    <Checkbox checked={selectedTicketIDs.has(ticket.id)} className="size-5 bg-muted" />
                                </TableCell>
                            )}
                            <TableCell className={`${!edit ? "pl-5" : ""}`}>{ticket.id}</TableCell>
                            <TableCell className="truncate max-w-50">{ticket.title}</TableCell>
                            <TableCell>
                                <span
                                    className={`${selectStatusBGColor(ticket.status)} py-1 px-2 rounded-xl text-center`}
                                >
                                    {ticket.status}
                                </span>
                            </TableCell>
                            {showFullTable && <TableCell className="text-lef">{ticket.category}</TableCell>}
                            <TableCell className="text-right">{ticket.createdAt}</TableCell>
                            {showFullTable && <TableCell className="text-right">{ticket.updatedAt}</TableCell>}
                            <TableCell className="pr-5">
                                <div className="flex flex-row items-center justify-end">
                                    <div
                                        className={`size-3 rounded-full ${selectRoleBGColor(ticket.assignedTo?.role)}`}
                                    />
                                    {ticket.assignedTo?.name || "None"}
                                </div>
                            </TableCell>
                            {showActionColumn && (
                                <TableCell className="flex items-center justify-end pr-5">
                                    <Button
                                        variant="ghost"
                                        className={`size-7 hover:size-8 transition-all ${
                                            openedActionTicket?.id === ticket.id && "bg-primary hover:bg-primary"
                                        }`}
                                        onClick={(e) => handleAction(e, ticket)}
                                    >
                                        <Ellipsis className="size-6" />
                                    </Button>
                                </TableCell>
                            )}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            {displayTickets.length === 0 && (
                <div className="flex justify-center items-center h-full bg-card border rounded-xl text-xl">
                    No available tickets
                </div>
            )}
        </div>
    );
};

export { TicketTable };
