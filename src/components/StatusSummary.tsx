import type { StatusSummaryType } from "@/types";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

type StatusSummaryProps = {
    statusSummaries: StatusSummaryType[];
};

const StatusSummary = ({ statusSummaries }: StatusSummaryProps) => {
    return (
        <div className="grid grid-cols-2 gap-2 h-full sm:grid-cols-4 sm:gap-4">
            {statusSummaries.map((summary: StatusSummaryType) => (
                <Card key={summary.status} className="grow gap-0 h-full">
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

export { StatusSummary };
