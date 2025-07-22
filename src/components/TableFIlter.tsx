import { useFilterContext } from "@/contexts/FilterContext";
import { useTicketContext } from "@/contexts/TicketContext";
import { Card, CardContent, CardDescription, CardTitle } from "@/components/ui/card";
import { Button } from "./ui/button";
import { RotateCcw } from "lucide-react";
import { getYearOptions, monthOptions } from "@/data/filterOptions";
import { useCallback, useEffect, useState } from "react";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import type { TicketType } from "@/types";

const yearOptions = getYearOptions();

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
                    } else {
                        setSelectedFilterByMonth("None");
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

    // reset selection when isReset is true
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
            if (filters.length === 0) {
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

type TableFilterProps = {
    padding?: string;
    hasBorder?: boolean;
    bgColor?: string;
};

const TableFilter = ({ padding, hasBorder = true, bgColor = "bg-card" }: TableFilterProps) => {
    const { origTickets, setDisplayTickets } = useTicketContext();
    const { setIsReset } = useFilterContext();

    const handleResetClick = () => {
        setIsReset(true);
        setDisplayTickets(origTickets);
    };

    return (
        <Card
            className={`px-6 gap-0 h-full flex flex-col justify-evenly ${bgColor}
                ${!hasBorder && "border-none"} ${padding || ""}`}
        >
            {/* title and reset  */}
            <CardTitle className="flex justify-between text-2xl text-primary">
                <span>Table Filters</span>
                <Button
                    onClick={handleResetClick}
                    className="bg-primary hover:bg-primary hover:ring-2 hover:ring-primary active:bg-primary/50 active:ring-primary/50"
                >
                    <span>reset</span>
                    <RotateCcw className="scale-125" />
                </Button>
            </CardTitle>

            <CardContent className="flex flex-col justify-evenly gap-2">
                {/* by status  */}
                <CardDescription className="text-lg">By status</CardDescription>
                <FilterSelection filterType="Status" values={["Open", "In progress", "Resolved", "Closed"]} />

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

export { TableFilter };
