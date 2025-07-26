import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { useTicketContext } from "@/contexts/TicketContext";
import { selectRoleBGColor } from "@/lib/utils";
import type { FileType } from "@/types";

type TicketDetailType =
    | "id"
    | "title"
    | "status"
    | "category"
    | "description"
    | "createdAt"
    | "updatedAt"
    | "assignedTo";

const Detail = ({ detail }: { detail: TicketDetailType }) => {
    const { openedActionTicket } = useTicketContext();

    return (
        <CardDescription className="flex flex-row gap-2 items-center">
            <span className="text-lg">{detail === "id" ? "ID" : detail[0].toUpperCase() + detail.slice(1)}</span>
            <div className="flex-1 bg-muted border border-input rounded-xl py-0.5 px-4 overflow-x-auto">
                <span className="text-foreground text-lg whitespace-nowrap">
                    {detail === "assignedTo" ? openedActionTicket?.assignedTo?.name : openedActionTicket?.[detail]}
                </span>
            </div>
        </CardDescription>
    );
};

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

            <Detail detail="id" />
            <Detail detail="title" />
            <Detail detail="status" />
            <Detail detail="category" />

            <CardDescription className="min-h-0 flex-1 flex flex-row gap-2">
                <span className="text-lg">Description:</span>
                <div className="overflow-y-auto bg-muted border border-input rounded-xl py-0.5 px-4">
                    <span className="text-foreground text-lg">{openedActionTicket?.description}</span>
                </div>
            </CardDescription>

            <CardDescription className="min-h-0 flex-1 flex flex-row gap-2">
                <span className="text-lg">Files:</span>
                <div className="flex-1 overflow-auto flex flex-col gap-2 bg-muted border border-input rounded-xl py-0.5 px-4">
                    {openedActionTicket?.files?.map((file: FileType) => {
                        return (
                            <span className="bg-accent text-foreground text-lg p-1 whitespace-nowrap">{file.name}</span>
                        );
                    })}
                </div>
            </CardDescription>

            <Detail detail="createdAt" />
            <Detail detail="updatedAt" />

            <CardDescription className="flex flex-row gap-2 items-center">
                <span className="text-lg">assignedTo:</span>
                <div className="flex-1 overflow-x-auto flex flex-row items-center bg-muted border border-input rounded-xl py-0.5 px-4">
                    <span className="text-foreground text-lg whitespace-nowrap">
                        {openedActionTicket?.assignedTo.name}
                    </span>
                    <div
                        className={`size-3 rounded-full ${
                            openedActionTicket && selectRoleBGColor(openedActionTicket.assignedTo.role)
                        }`}
                    />
                    <span className="text-foreground text-lg whitespace-nowrap">
                        {openedActionTicket?.assignedTo.role}
                    </span>
                </div>
            </CardDescription>
        </Card>
    );
};

export { TicketDetails };
