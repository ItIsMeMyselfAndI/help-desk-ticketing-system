import { useState } from "react";
import type { StatusSummaryType } from "@/types";
import { FilterProvider } from "@/contexts/FilterContext";
import { StatusSummary } from "@/components/StatusSummary";
import { TicketTable } from "@/components/TicketTable";
import { TableFilter } from "@/components/TableFIlter";
import { QuickEditSection } from "@/components/QuickEdit";

const HomePage = () => {
    const [statusSummaries] = useState<StatusSummaryType[]>([
        { status: "Open", count: 0 },
        { status: "In progress", count: 0 },
        { status: "Resolved", count: 0 },
        { status: "Closed", count: 0 },
    ]);

    return (
        <div className="h-[100vh] p-4 grid grid-rows-6 gap-2 sm:grid-rows-5 sm:gap-4">
            <div className="row-span-2 sm:row-span-1">
                <StatusSummary statusSummaries={statusSummaries} />
            </div>
            <div className="row-span-4 grid grid-cols-4 gap-2 sm:row-span-4 sm:gap-4">
                <div className="col-span-4 xl:col-span-3 overflow-auto">
                    <TicketTable edit={true} />
                </div>
                <div className="hidden xl:col-span-1 xl:grid grid-rows-2 gap-4">
                    <div className="row-span-1 flex-10">
                        <FilterProvider>
                            <TableFilter />
                        </FilterProvider>
                    </div>
                    <div className="row-span-1 flex-1 w-full h-full">
                        <QuickEditSection />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomePage;
