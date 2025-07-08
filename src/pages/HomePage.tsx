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
import React, { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { RotateCcw, Ticket } from "lucide-react";

type Ticket = {
    id: string;
    title: string;
    status: "Unassigned" | "In Progress" | "Resolved" | "Closed";
    created_at: string;
    updated_at: string;
    assigned_to: string;
};

const populateTicketArr = (arr: Ticket[], count: number) => {
    const populatedArr: Ticket[] = [];
    for (let i = 0; i < count; i++) {
        arr.forEach((t) => populatedArr.push({ ...t }));
    }
    populatedArr.forEach((ticket, index) => (ticket.id = `T-${index}`));
    return populatedArr;
};

type TicketContextType = {
    origTickets: Ticket[];
    setOrigTickets: React.Dispatch<React.SetStateAction<Ticket[]>>;
    copyTickets: Ticket[];
    setCopyTickets: React.Dispatch<React.SetStateAction<Ticket[]>>;
};

const TicketContext = createContext<TicketContextType | undefined>(undefined);

const TicketProvider = ({ children }: { children: ReactNode }) => {
    const defaultTickets: Ticket[] = populateTicketArr(
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
    const [origTickets, setOrigTickets] = useState<Ticket[]>([...defaultTickets]);
    const [copyTickets, setCopyTickets] = useState<Ticket[]>([...defaultTickets]);
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

type SummaryCardProps = {
    status: string;
    count: number;
};

const SummaryCard = ({ status, count }: SummaryCardProps) => {
    return (
        <Card className="grow gap-0 h-50">
            <CardHeader className="text-foreground/80 text-xl leading-none text-left">{status}</CardHeader>
            <CardContent className="flex text-primary justify-center text-5xl leading-none m-auto">{count}</CardContent>
        </Card>
    );
};

type SummarySectionProps = {
    statusSummaries: statusSummary[];
};

const SummarySection = ({ statusSummaries }: SummarySectionProps) => {
    return (
        <div className="flex gap-4">
            {statusSummaries.map((summary: statusSummary) => (
                <SummaryCard status={summary.status} count={summary.count}></SummaryCard>
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

    const chooseStatusColor = (status: Ticket["status"]) => {
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
        <Table className="bg-card">
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
        <Card className="px-6 gap-0">
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

type statusSummary = {
    status: string;
    count: number;
};

const HomePage = () => {
    const [statusSummaries, setStatusSummaries] = useState<statusSummary[]>([
        { status: "Unassigned", count: 0 },
        { status: "In progress", count: 0 },
        { status: "Resolved", count: 0 },
        { status: "Closed", count: 0 },
    ]);

    return (
        <TicketProvider>
            <div className="flex flex-col gap-4 h-full w-full">
                <SummarySection statusSummaries={statusSummaries} />
                <div className="flex min-h-0 gap-4">
                    <div className="flex-4 bg-card item overflow-auto">
                        <TicketTable />
                    </div>
                    <div className="flex-1 flex flex-col justify-evenly gap-4 h-full w-full">
                        <FiltersCard />
                        <div className="flex-1 w-full h-full bg-card border rounded-xl"></div>
                    </div>
                </div>
            </div>
        </TicketProvider>
    );
};

export default HomePage;
