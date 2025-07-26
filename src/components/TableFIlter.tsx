import { useFilterContext } from "@/contexts/FilterContext";
import { useTickets } from "@/hooks/use-tickets";
import { Card, CardAction, CardContent, CardDescription, CardTitle } from "@/components/ui/card";
import { Button } from "./ui/button";
import { RotateCcw } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import type { TicketType } from "@/types";
import { Selector } from "./Selector";
import { ASSIGNMENT_TO, CATEGORIES, MONTHS, STATUSES, YEARS } from "@/data/constants";

type FilterSelectionProps = {
    filterType: "status" | "category" | "year" | "month" | "assignment";
    options: string[];
};

const FilterSelection = ({ filterType, options }: FilterSelectionProps) => {
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
    const { origTickets, setDisplayTickets } = useTickets();
    const [selectedItem, setSelectedItem] = useState<string>(defaultItem);

    const updateFilterContext = useCallback(
        (value: string) => {
            switch (filterType.toLowerCase()) {
                case "status":
                    setSelectedFilterByStatus(value);
                    break;
                case "category":
                    setSelectedFilterByStatus(value);
                    break;
                case "year":
                    setSelectedFilterByYear(value);
                    break;
                case "month": {
                    const monthIndex = MONTHS.indexOf(value);
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
                    const [year, month] = ticket.createdAt.split("-");
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
        <CardAction className="h-full w-full flex flex-col gap-2">
            <CardDescription className="text-lg">By {filterType}</CardDescription>
            <Selector
                options={options}
                defaultItem="None"
                selectedItem={selectedItem}
                handleSelectionChange={handleSelectionChange}
                filterType={filterType}
            />
        </CardAction>
    );
};

type TableFilterProps = {
    padding?: string;
    hasBorder?: boolean;
    bgColor?: string;
    variant?: "default" | "full";
};

const TableFilter = ({ padding, hasBorder = true, bgColor = "bg-card", variant = "default" }: TableFilterProps) => {
    const { origTickets, setDisplayTickets } = useTickets();
    const { setIsReset } = useFilterContext();

    const handleResetClick = () => {
        setIsReset(true);
        setDisplayTickets(origTickets);
    };

    return (
        <Card
            className={`px-6 gap-2 h-full flex flex-col ${bgColor}
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

            <CardContent className="flex-1 flex flex-col justify-evenly gap-2">
                {/* by status  */}
                <section className={`flex-1 ${variant === "full" && "flex flex-row gap-2"}`}>
                    <FilterSelection filterType="status" options={STATUSES} />
                    {variant === "full" && <FilterSelection filterType="category" options={CATEGORIES} />}
                </section>

                {/* by date  */}
                <section className="flex-1 flex flex-row gap-2">
                    <FilterSelection filterType="year" options={YEARS} />
                    <FilterSelection filterType="month" options={MONTHS} />
                </section>

                {/* by assignment */}
                <section className="flex-1">
                    <FilterSelection filterType="assignment" options={ASSIGNMENT_TO} />
                </section>
            </CardContent>
        </Card>
    );
};

export { TableFilter };
