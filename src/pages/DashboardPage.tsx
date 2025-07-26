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
        <main className="h-[100vh] p-4 flex flex-col gap-2 md:gap-4">
            <section className="xl:h-40">
                <StatusSummary statusSummaries={statusSummaries} />
            </section>
            <section className="flex-1 min-h-0 grid grid-cols-1 bg-amber-600">
                <div className="min-h-0 flex flex-row gap-4">
                    {/* table */}
                    <div className={`overflow-auto flex-1`}>
                        <TicketTable edit={true} />
                    </div>
                    {/* action */}
                    <div className="hidden flex-1 min-w-md max-w-md xl:grid grid-rows-2 gap-4">
                        <FilterProvider>
                            <TableFilter />
                        </FilterProvider>
                        <QuickEdit />
                    </div>
                </div>
            </section>
        </main>
    );
};

export default DashboardPage;
