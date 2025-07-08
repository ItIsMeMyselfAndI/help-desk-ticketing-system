import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectLabel,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { DatePicker } from "@/components/ui/date-picker";
import { Checkbox } from "@/components/ui/checkbox";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { RotateCcw } from "lucide-react";
import type { StatusSummaryType, TicketType } from "@/types";
import { TicketProvider, useTicketContext } from "@/contexts/TicketContext";

type SummaryCardProps = {
    status: string;
    count: number;
};

const SummaryCard = ({ status, count }: SummaryCardProps) => {
    return (
        <Card className="grow gap-0 h-full">
            <CardHeader className="text-foreground/80 text-xl leading-none text-left">{status}</CardHeader>
            <CardContent className="flex text-primary justify-center text-5xl leading-none m-auto">{count}</CardContent>
        </Card>
    );
};

type SummarySectionProps = {
    statusSummaries: StatusSummaryType[];
};

const SummarySection = ({ statusSummaries }: SummarySectionProps) => {
    return (
        <div className="grid grid-cols-4 gap-4 h-full">
            {statusSummaries.map((summary: StatusSummaryType) => (
                <SummaryCard status={summary.status} count={summary.count} />
            ))}
        </div>
    );
};

const TicketTable = () => {
    const { copyTickets } = useTicketContext();
    const [selectedRows, setSelectedRows] = useState<Set<string>>(new Set());

    const toggleRowSelection = (id: string) => {
        setSelectedRows((prev) => {
            const selectedRowsCopy = new Set(prev); // Create a copy
            if (selectedRowsCopy.has(id)) {
                selectedRowsCopy.delete(id);
            } else {
                selectedRowsCopy.add(id);
            }
            return selectedRowsCopy; // Return the new Set
        });
    };

    const chooseStatusColor = (status: TicketType["status"]) => {
        switch (status) {
            case "Unassigned":
                return "bg-gray-500";
            case "In Progress":
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
            <Table className="bg-card w-full">
                <TableHeader className="text-xl bg-muted h-15">
                    <TableRow key="header">
                        <TableHead className="text-primary pl-5">Edit</TableHead>
                        <TableHead className="text-primary">Ticket</TableHead>
                        <TableHead className="text-primary">Title</TableHead>
                        <TableHead className="text-primary">Status</TableHead>
                        <TableHead className="text-primary">Submitted At</TableHead>
                        <TableHead className="text-primary text-right pr-5">Assigned To</TableHead>
                    </TableRow>
                </TableHeader>

                <TableBody className="text-lg">
                    {copyTickets.map((ticket) => (
                        <TableRow key={ticket.id} onClick={() => toggleRowSelection(ticket.id)}>
                            <TableCell className="pl-5">
                                <Checkbox checked={selectedRows.has(ticket.id)} className="size-5 bg-muted" />
                            </TableCell>
                            <TableCell>{ticket.id}</TableCell>
                            <TableCell>{ticket.title}</TableCell>
                            <TableCell>
                                <span className={`${chooseStatusColor(ticket.status)} p-1 rounded-xl text-center`}>
                                    {ticket.status}
                                </span>
                            </TableCell>
                            <TableCell>{ticket.created_at}</TableCell>
                            <TableCell className="text-right pr-5">{ticket.assigned_to}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            {copyTickets.length === 0 && (
                <div className="flex justify-center items-center h-full bg-card border rounded-lg text-xl">
                    No available tickets
                </div>
            )}
        </div>
    );
};

type FilterSelectionProps = {
    placeholder: string;
    values: string[];
};

const FilterSelection = ({ placeholder, values }: FilterSelectionProps) => {
    const { origTickets, setCopyTickets } = useTicketContext();
    const [selectedItem, setSelectedItem] = useState<string>("");

    useEffect(() => {
        if (!selectedItem) {
            setCopyTickets(origTickets);
            return;
        }
        const filteredTickets = origTickets.filter((ticket) => {
            switch (selectedItem.toLowerCase()) {
                case ticket.status.toLowerCase():
                    return ticket;
                case ticket.created_at.toLowerCase():
                    return ticket;
                case ticket.assigned_to.toLowerCase():
                    return ticket;
                default:
                    return;
            }
        });
        filteredTickets.forEach((ticket) => console.log(ticket));
        setCopyTickets(filteredTickets);
    }, [selectedItem, origTickets]);

    return (
        <Select value={selectedItem} onValueChange={setSelectedItem}>
            <SelectTrigger className="w-full text-foreground data-[size=default]:h-full bg-muted hover:bg-accent">
                <SelectValue placeholder={`Select ${placeholder}`} className="text-foreground/50" />
            </SelectTrigger>

            <SelectContent>
                <SelectGroup>
                    <SelectLabel className="text-lg text-foreground/50">{placeholder}</SelectLabel>
                    {values.map((val: string) => (
                        <SelectItem className="focus:bg-primary" value={val.toLowerCase()}>
                            {val}
                        </SelectItem>
                    ))}
                </SelectGroup>
            </SelectContent>
        </Select>
    );
};

const FiltersCard = () => {
    const { origTickets, setCopyTickets } = useTicketContext();
    const handleResetClick = () => {
        setCopyTickets(origTickets);
    };

    return (
        <Card className="px-6 gap-0 h-full flex flex-col justify-evenly">
            {/* title and reset  */}
            <CardTitle className="flex justify-between text-2xl text-primary">
                <span>Table Filters</span>
                <Button onClick={handleResetClick} className="bg-primary hover:bg-primary/80 active:bg-primary/50">
                    <span>reset</span>
                    <RotateCcw className="scale-125" />
                </Button>
            </CardTitle>

            <CardContent className="flex flex-col justify-evenly gap-2">
                {/* by status  */}
                <CardDescription className="text-lg">By status</CardDescription>
                <FilterSelection placeholder="Status" values={["Unassigned", "In progress", "Resolved", "Closed"]} />

                {/* by date  */}
                <CardDescription className="text-lg">By date submitted</CardDescription>
                <DatePicker placeholder="Date" />

                {/* by assignment */}
                <CardDescription className="text-lg">By assignment</CardDescription>
                <FilterSelection placeholder="Assignment" values={["@johndoe", "@dora", "@patric", "@spongebob"]} />
            </CardContent>
        </Card>
    );
};

const HomePage = () => {
    const [statusSummaries, setStatusSummaries] = useState<StatusSummaryType[]>([
        { status: "Unassigned", count: 0 },
        { status: "In progress", count: 0 },
        { status: "Resolved", count: 0 },
        { status: "Closed", count: 0 },
    ]);

    return (
        <TicketProvider>
            <div className="grid grid-rows-5 gap-4 h-[100vh] content-stretch p-4">
                <div className="row-span-1">
                    <SummarySection statusSummaries={statusSummaries} />
                </div>
                <div className="row-span-4 grid grid-cols-4 gap-4">
                    <div className="col-span-3 overflow-auto h-full">
                        <TicketTable />
                    </div>
                    <div className="col-span-1 grid grid-rows-2 gap-4">
                        <div className="row-span-1 flex-10">
                            <FiltersCard />
                        </div>
                        <div className="row-span-1 flex-1">
                            <div className="w-full h-full bg-card border rounded-xl"></div>
                        </div>
                    </div>
                </div>
            </div>
        </TicketProvider>
    );
};

export default HomePage;
