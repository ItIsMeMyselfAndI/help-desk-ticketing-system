import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { useTicketContext } from "@/contexts/TicketContext";
import { selectRoleBGColor } from "@/lib/utils";

type TicketDetailsProps = {
    padding?: string;
    hasBorder?: boolean;
};

const TicketDetails = ({ padding, hasBorder = true }: TicketDetailsProps) => {
    const { openedActionTicket } = useTicketContext();

    return (
        <Card className={`size-full flex flex-col gap-2 ${padding || "p-4"} ${!hasBorder && "border-none"}`}>
            <CardTitle className="flex justify-start">
                <span className="text-primary text-2xl">Details</span>
            </CardTitle>

            <CardDescription className="flex flex-row gap-2 items-center">
                <span className="text-lg">ID:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedActionTicket?.id}</span>
                </div>
            </CardDescription>

            <CardDescription className=" flex flex-row gap-2 items-center">
                <span className="text-lg">Status:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedActionTicket?.status}</span>
                </div>
            </CardDescription>

            <CardDescription className="flex flex-row gap-2 items-center">
                <span className="text-lg">Title:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedActionTicket?.title}</span>
                </div>
            </CardDescription>

            <CardDescription className="min-h-0 flex-1 flex flex-row gap-2">
                <span className="text-lg">Description:</span>
                <div className="overflow-y-auto bg-muted border border-input rounded-xl py-0.5 px-4">
                    <span className="text-foreground text-lg">{openedActionTicket?.description}</span>
                </div>
            </CardDescription>

            <CardDescription className="flex flex-row gap-2 items-center">
                <span className="text-lg">Created at:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedActionTicket?.created_at}</span>
                </div>
            </CardDescription>

            <CardDescription className="flex flex-row gap-2 items-center min-w-0">
                <span className="text-lg">Updated at:</span>
                <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                    <span className="text-foreground text-lg whitespace-nowrap">{openedActionTicket?.updated_at}</span>
                </div>
            </CardDescription>

            <CardDescription className="flex flex-row gap-2 items-center">
                <span className="text-lg">Assigned to:</span>
                <div className="flex-1 overflow-x-auto flex flex-row items-center bg-muted border border-input rounded-xl py-0.5 px-4">
                    <span className="text-foreground text-lg whitespace-nowrap">
                        {openedActionTicket?.assigned_to.name}
                    </span>
                    <div
                        className={`size-3 rounded-full ${
                            openedActionTicket && selectRoleBGColor(openedActionTicket.assigned_to.role)
                        }`}
                    />
                    <span className="text-foreground text-lg whitespace-nowrap">
                        {openedActionTicket?.assigned_to.role}
                    </span>
                </div>
            </CardDescription>
        </Card>
    );
};

export { TicketDetails };
