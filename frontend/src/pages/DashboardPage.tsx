import { useState } from "react";
import type { StatusSummaryType } from "@/types";
import { StatusSummary } from "@/components/StatusSummary";
import { TicketTable } from "@/components/TicketTable";
import { Actions } from "@/components/Action";
import { APP_MIN_HEIGHT, MAIN_MIN_WIDTH } from "@/data/constants";

const DashboardPage = () => {
    const [statusSummaries] = useState<StatusSummaryType[]>([
        { status: "Open", count: 0 },
        { status: "In progress", count: 0 },
        { status: "Resolved", count: 0 },
        { status: "Closed", count: 0 },
    ]);

    return (
        <main
            className={`h-[100vh] p-4 flex flex-col gap-2 md:gap-4`}
            style={{ minHeight: APP_MIN_HEIGHT, minWidth: MAIN_MIN_WIDTH }}
        >
            <section className="xl:h-40">
                <StatusSummary statusSummaries={statusSummaries} />
            </section>
            <section className="flex-1 min-h-0 grid grid-cols-1">
                <div className="min-h-0 flex flex-row gap-4">
                    {/* table */}
                    <div className={`overflow-auto flex-1`}>
                        <TicketTable edit={true} />
                    </div>
                    {/* action */}
                    <div className="hidden flex-1 min-w-md max-w-md xl:block">
                        <Actions variant="default" />
                    </div>
                </div>
            </section>
        </main>
    );
};

export default DashboardPage;
