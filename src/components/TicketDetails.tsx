import type { TicketType } from "@/types";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";

type TicketDetailsProps = {
    openedTicket: TicketType | undefined;
    padding?: string;
    hasBorder?: boolean;
};

const TicketDetails = ({ openedTicket, padding, hasBorder = true }: TicketDetailsProps) => {
    return (
        <Card className={`size-full flex flex-col gap-2 ${padding || "p-4"} ${!hasBorder && "border-none"}`}>
            <CardTitle className="flex justify-start">
                <span className="text-primary text-2xl">Details</span>
            </CardTitle>
            <CardDescription className="flex flex-row gap-2 items-center">
                <span>ID:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedTicket?.id}</span>
                </div>
            </CardDescription>
            <CardDescription className="flex flex-row gap-2 items-center">
                <span>Title:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedTicket?.title}</span>
                </div>
            </CardDescription>
            <CardDescription className="flex flex-row gap-2 items-center">
                <span>Status:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedTicket?.status}</span>
                </div>
            </CardDescription>
            <CardDescription className="min-h-0 flex-1 flex flex-row gap-2">
                <span>Description:</span>
                <div className="overflow-y-auto bg-muted border border-input rounded-xl py-0.5 px-4">
                    <span className="text-foreground text-lg">{openedTicket?.description}</span>
                </div>
            </CardDescription>
            <CardDescription className="flex flex-row gap-2 items-center">
                <span>Created at:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedTicket?.created_at}</span>
                </div>
            </CardDescription>
            <CardDescription className="flex flex-row gap-2 items-center">
                <span>Updated at:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedTicket?.updated_at}</span>
                </div>
            </CardDescription>
            <CardDescription className="flex flex-row gap-2 items-center">
                <span>Assigned to:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedTicket?.assigned_to.name}</span>
                </div>
            </CardDescription>
        </Card>
    );
};

export { TicketDetails };
