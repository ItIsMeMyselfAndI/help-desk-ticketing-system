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
// import { DatePicker } from "@/components/ui/date-picker";
import { Checkbox } from "@/components/ui/checkbox";
import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { RotateCcw, Trash2Icon } from "lucide-react";
import type { StatusSummaryType, TicketType } from "@/types";
import { useTicketContext } from "@/contexts/TicketContext";
import { FilterProvider, useFilterContext } from "@/contexts/FilterContext";
import { getYearOptions, monthOptions } from "@/constants/filterOptions";

const yearOptions = getYearOptions();

type SummaryCardsSectionProps = {
    statusSummaries: StatusSummaryType[];
};

const SummaryCardsSection = ({ statusSummaries }: SummaryCardsSectionProps) => {
    return (
        <div className="grid grid-cols-2 gap-2 h-full sm:grid-cols-4 sm:gap-4">
            {statusSummaries.map((summary: StatusSummaryType) => (
                <Card className="grow gap-0 h-full">
                    <CardHeader className="text-foreground/80 leading-none text-left text-sm lg:text-xl">
                        {summary.status}
                    </CardHeader>
                    <CardContent className="flex text-primary justify-center leading-none m-auto text-3xl lg:text-5xl">
                        {summary.count}
                    </CardContent>
                </Card>
            ))}
        </div>
    );
};

const TicketTable = () => {
    const { displayTickets, selectedTicketIDs, setSelectedTicketIDs } = useTicketContext();

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
            case "Unassigned":
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
                        <TableHead className="text-primary pl-5">Edit</TableHead>
                        <TableHead className="text-primary">Ticket</TableHead>
                        <TableHead className="text-primary">Title</TableHead>
                        <TableHead className="text-primary">Status</TableHead>
                        <TableHead className="text-primary">Submitted At</TableHead>
                        <TableHead className="text-primary text-right pr-5">Assigned To</TableHead>
                    </TableRow>
                </TableHeader>

                <TableBody>
                    {displayTickets.map((ticket) => (
                        <TableRow key={ticket.id} onClick={() => toggleRowSelection(ticket.id)}>
                            <TableCell className="pl-5">
                                <Checkbox checked={selectedTicketIDs.has(ticket.id)} className="size-5 bg-muted" />
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
            {displayTickets.length === 0 && (
                <div className="flex justify-center items-center h-full bg-card border rounded-xl text-xl">
                    No available tickets
                </div>
            )}
        </div>
    );
};

type FilterSelectionProps = {
    filterType: string;
    values: string[];
};

const FilterSelection = ({ filterType, values }: FilterSelectionProps) => {
    const defaultItem = "None";
    const {
        // states
        isReset,
        selectedFilterByStatus,
        selectedFilterByYear,
        selectedFilterByMonth,
        selectedFilterByAssignment,
        // setters
        setIsReset,
        setSelectedFilterByStatus,
        setSelectedFilterByYear,
        setSelectedFilterByMonth,
        setSelectedFilterByAssignment,
    } = useFilterContext();
    const { origTickets, setDisplayTickets } = useTicketContext();
    const [selectedItem, setSelectedItem] = useState<string>(defaultItem);

    const updateFilterContext = useCallback(
        (value: string) => {
            switch (filterType.toLowerCase()) {
                case "status":
                    setSelectedFilterByStatus(value);
                    break;
                case "year":
                    setSelectedFilterByYear(value);
                    break;
                case "month": {
                    const monthIndex = monthOptions.indexOf(value);
                    if (monthIndex !== -1) {
                        setSelectedFilterByMonth(String(monthIndex + 1).padStart(2, "0"));
                    }
                    break;
                }
                case "assignment":
                    setSelectedFilterByAssignment(value);
                    break;
                default:
                    break;
            }
        },
        [
            filterType,
            setSelectedFilterByStatus,
            setSelectedFilterByYear,
            setSelectedFilterByMonth,
            setSelectedFilterByAssignment,
        ]
    );

    useEffect(() => {
        if (isReset) {
            setSelectedItem(defaultItem);
            setIsReset(false);
            updateFilterContext(defaultItem);
        }
    }, [isReset, setIsReset, setSelectedItem, updateFilterContext]);

    useEffect(() => {
        // update ticket table display
        let filteredTickets: TicketType[];
        if (!selectedItem) {
            filteredTickets = origTickets;
        } else {
            // get all filters
            const filters = [
                selectedFilterByStatus,
                selectedFilterByYear,
                selectedFilterByMonth,
                selectedFilterByAssignment,
            ].filter((val) => val !== "None" && val !== "");
            if (filters.every((val) => val === "None")) {
                filteredTickets = origTickets;
            }
            console.log(filters);
            // filter tickets
            filteredTickets = origTickets.filter((ticket) =>
                filters.every((val) => {
                    const [year, month] = ticket.created_at.split("-");
                    if (Object.values(ticket).includes(val) || year === val || month === val) {
                        return true;
                    }
                    return false;
                })
            );
        }
        setDisplayTickets(filteredTickets);
    }, [
        selectedItem,
        origTickets,
        setDisplayTickets,
        selectedFilterByStatus,
        selectedFilterByYear,
        selectedFilterByMonth,
        selectedFilterByAssignment,
    ]);

    const handleSelectionChange = (value: string) => {
        updateFilterContext(value);
        setSelectedItem(value);
    };

    return (
        <Select value={selectedItem} onValueChange={handleSelectionChange}>
            <SelectTrigger
                className={`w-full text-foreground data-[size=default]:h-full bg-muted hover:bg-accent ${
                    selectedItem === defaultItem && "text-muted-foreground"
                }`}
            >
                <SelectValue placeholder={defaultItem} />
            </SelectTrigger>
            <SelectContent>
                <SelectGroup>
                    <SelectLabel className="text-lg text-foreground/50">{`Select ${filterType}`}</SelectLabel>
                    <SelectItem
                        className="text-muted-foreground focus:bg-accent focus:text-muted-foreground"
                        value={defaultItem}
                    >
                        None
                    </SelectItem>
                    {values.map((val: string) => (
                        <SelectItem key={val.toLowerCase()} className="focus:bg-primary" value={val}>
                            {val}
                        </SelectItem>
                    ))}
                </SelectGroup>
            </SelectContent>
        </Select>
    );
};

const FiltersCard = () => {
    const { origTickets, setDisplayTickets } = useTicketContext();
    const { setIsReset } = useFilterContext();

    const handleResetClick = () => {
        setIsReset(true);
        setDisplayTickets(origTickets);
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
                <FilterSelection filterType="Status" values={["Unassigned", "In progress", "Resolved", "Closed"]} />

                {/* by date  */}
                <div className="grid grid-cols-2 gap-2">
                    <CardDescription className="text-lg">By year</CardDescription>
                    <CardDescription className="text-lg">By month</CardDescription>
                    <FilterSelection filterType="Year" values={yearOptions} />
                    <FilterSelection filterType="Month" values={monthOptions} />
                </div>

                {/* by assignment */}
                <CardDescription className="text-lg">By assignment</CardDescription>
                <FilterSelection filterType="Assignment" values={["@bentot", "@juantot", "@gwentot", "@kwintot"]} />
            </CardContent>
        </Card>
    );
};

const StatusChangeSelection = () => {
    const defaultItem = "None";
    const [selectedItem, setSelectedItem] = useState<string>(defaultItem);

    const handleSelectionChange = (value: string) => {
        setSelectedItem(value);
    };

    const statuses = ["Re-open", "Close"];

    return (
        <Select value={selectedItem} onValueChange={handleSelectionChange}>
            <SelectTrigger
                className={`w-full text-foreground data-[size=default]:h-full bg-muted hover:bg-accent ${
                    selectedItem === defaultItem && "text-muted-foreground"
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

const QuickEditCard = () => {
    const { origTickets, setOrigTickets, selectedTicketIDs, setSelectedTicketIDs, isAllSelected, setIsAllSelected } =
        useTicketContext();

    const toggleSelectAll = () => {
        if (isAllSelected) {
            setSelectedTicketIDs(new Set());
            setIsAllSelected(false);
        } else {
            setSelectedTicketIDs(new Set(origTickets.map((ticket) => ticket.id)));
            setIsAllSelected(true);
        }
    };

    return (
        <Card className="px-6 gap-0 h-full flex flex-col justify-evenly">
            <CardTitle className="flex justify-between text-2xl text-primary">
                <span>Quick Edit</span>
                <section className="flex items-center justify-end gap-2">
                    <CardDescription className="text-lg font-medium">Select all tickets</CardDescription>
                    <Checkbox className="size-5 bg-muted" onClick={toggleSelectAll} />
                </section>
            </CardTitle>

            <CardContent className="flex flex-col justify-evenly gap-4">
                <section className="flex-1 flex flex-col gap-1">
                    <CardDescription className="text-lg">Change status</CardDescription>
                    <StatusChangeSelection />
                </section>

                <section className="grid grid-cols-2 gap-2 flex-1">
                    <Button className="h-full bg-green-500 hover:bg-green-500 hover:ring-4 hover:ring-green-500 active:bg-green-600 active:ring-green-600">
                        <span className="text-foreground">Update</span>
                    </Button>
                    <Button className="h-full bg-yellow-500 hover:bg-yellow-500 hover:ring-4 hover:ring-yellow-500 active:bg-yellow-600 active:ring-yellow-600">
                        <span className="text-foreground">Cancel</span>
                    </Button>
                </section>

                <section className="flex flex-col flex-1">
                    <CardDescription className="text-lg">Delete</CardDescription>
                    <Button className="bg-red-500 hover:bg-red-500 hover:ring-4 hover:ring-red-500 active:bg-red-600 active:ring-red-600">
                        <Trash2Icon className="scale-150" />
                    </Button>
                </section>
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
        <div className="grid grid-rows-6 gap-2 h-[100vh] content-stretch p-4 sm:grid-rows-5 sm:gap-4">
            <div className="row-span-2 sm:row-span-1">
                <SummaryCardsSection statusSummaries={statusSummaries} />
            </div>
            <div className="row-span-4 grid grid-cols-4 gap-2 sm:row-span-4 sm:gap-4">
                <div className="col-span-4 xl:col-span-3 overflow-auto">
                    <TicketTable />
                </div>
                <div className="hidden xl:col-span-1 xl:grid grid-rows-2 gap-4">
                    <div className="row-span-1 flex-10">
                        <FilterProvider>
                            <FiltersCard />
                        </FilterProvider>
                    </div>
                    <div className="row-span-1 flex-1 w-full h-full">
                        <QuickEditCard />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomePage;
