import { useTicketContext } from "@/contexts/TicketContext";
import type { TicketType } from "@/types";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "./ui/button";
import MessageFilled from "@/assets/message-write-svgrepo-com.svg";

type TicketTableProps = {
    edit?: true | false;
    variant?: "default" | "message" | "full" | "combo";
};

const TicketTable = ({ edit = false, variant = "default" }: TicketTableProps) => {
    const { displayTickets, selectedTicketIDs, setSelectedTicketIDs } = useTicketContext();

    const showFullTable = variant === "full" || variant === "combo";
    const showMessageColumn = variant === "message" || variant === "combo";

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

    const chooseStatusColor = (status: TicketType["status"]) => {
        switch (status) {
            case "Open":
                return "bg-gray-500";
            case "In progress":
                return "bg-blue-500";
            case "Resolved":
                return "bg-green-500";
            case "Closed":
                return "bg-yellow-500";
            default:
                return "";
        }
    };

    return (
        <div className="h-full flex flex-col gap-2">
            <Table className="bg-card w-full text-sm lg:text-lg">
                <TableHeader className="bg-muted h-15 sticky top-0 z-1">
                    <TableRow key="header" className="text-lg lg:text-xl">
                        {edit && <TableHead className="text-primary pl-5">Edit</TableHead>}
                        <TableHead className="text-primary">Ticket</TableHead>
                        <TableHead className="text-primary">Title</TableHead>
                        <TableHead className="text-primary">Status</TableHead>
                        <TableHead className="text-primary">Submitted At</TableHead>
                        {showFullTable && <TableHead className="text-primary">Updated At</TableHead>}
                        <TableHead className="text-primary text-right pr-5">Assigned To</TableHead>
                        {showMessageColumn && <TableHead className="text-primary text-right pr-5">Message</TableHead>}
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
                            <TableCell>{ticket.id}</TableCell>
                            <TableCell>{ticket.title}</TableCell>
                            <TableCell>
                                <span className={`${chooseStatusColor(ticket.status)} p-1 rounded-xl text-center`}>
                                    {ticket.status}
                                </span>
                            </TableCell>
                            <TableCell>{ticket.created_at}</TableCell>
                            {showFullTable && <TableCell>{ticket.updated_at}</TableCell>}
                            <TableCell className="text-right pr-5">{ticket.assigned_to}</TableCell>
                            {showMessageColumn && (
                                <TableCell className="flex items-center justify-end pr-5">
                                    <Button variant="ghost" className="hover:bg-transparent">
                                        <img
                                            src={MessageFilled}
                                            alt="Message Icon"
                                            className="size-7 hover:size-9 transition-all"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                window.alert(`message clicked: ${ticket.id}`);
                                            }}
                                        />
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
