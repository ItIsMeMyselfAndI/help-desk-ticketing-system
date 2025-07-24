import { useState } from "react";
import type { StatusSummaryType } from "@/types";
import { FilterProvider } from "@/contexts/FilterContext";
import { StatusSummary } from "@/components/StatusSummary";
import { TicketTable } from "@/components/TicketTable";
import { TableFilter } from "@/components/TableFIlter";
import { QuickEdit } from "@/components/QuickEdit";

const DashboardPage = () => {
    const [statusSummaries] = useState<StatusSummaryType[]>([
        { status: "Open", count: 0 },
        { status: "In progress", count: 0 },
        { status: "Resolved", count: 0 },
        { status: "Closed", count: 0 },
    ]);

    return (
        <div className="h-[100vh] p-4 flex flex-col gap-2 sm:gap-4">
            <div>
                <StatusSummary statusSummaries={statusSummaries} />
            </div>
            <div className="min-h-0 grid grid-cols-1">
                <div className="min-h-0 flex-1 flex flex-row gap-4">
                    {/* table */}
                    <div className={`overflow-auto flex-1`}>
                        <TicketTable edit={true} />
                    </div>
                    {/* action */}
                    <div className="hidden flex-1 min-w-md max-w-md xl:grid grid-row-2 gap-4">
                        <FilterProvider>
                            <TableFilter />
                        </FilterProvider>
                        <QuickEdit />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;
