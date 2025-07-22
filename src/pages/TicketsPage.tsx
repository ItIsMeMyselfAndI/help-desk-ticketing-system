import { TicketTable } from "@/components/TicketTable";
import { Card, CardAction, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { selectStatusBGColor } from "@/lib/utils";
import type { TicketType } from "@/types";
import { useState } from "react";
import CloseXSVG from "@/assets/close-circle-svgrepo-com.svg";
import { ImageButton } from "@/components/ImageButton";
import SendSVG from "@/assets/send-svgrepo-com.svg";
import { Button } from "@/components/ui/button";
import { FilterProvider } from "@/contexts/FilterContext";
import { Separator } from "@/components/ui/separator";
import { TableFilter } from "@/components/TableFIlter";
import { QuickEditSection } from "@/components/QuickEdit";

type ActionProps = {
    openedTicket: TicketType | undefined;
    onActionExitClick?: (ticket: TicketType | undefined) => void;
};

const Header = ({ openedTicket, onActionExitClick }: ActionProps) => {
    return (
        <header className="text-2xl grid grid-rows-2 gap-1">
            <section className="flex flex-row justify-between items-center">
                <h3 className="text-primary">Actions</h3>
                <ImageButton
                    path={CloseXSVG}
                    alt="X"
                    className="size-9 hover:size-10 transition-all"
                    onClick={() => onActionExitClick?.(openedTicket)}
                />
            </section>
            <section className="flex flex-row justify-between items-center">
                <span className="text-lg">{openedTicket ? openedTicket.id : "None"}</span>
                {openedTicket ? (
                    <span
                        className={`${selectStatusBGColor(
                            openedTicket.status
                        )} font-normal py-1 px-2 rounded-xl text-center`}
                    >
                        {openedTicket.status}
                    </span>
                ) : (
                    <span>Ticket not found</span>
                )}
            </section>
        </header>
    );
};

const Message = ({ openedTicket }: ActionProps) => {
    return (
        <Card className="size-full p-4 text-xl flex flex-col gap-3">
            <CardTitle className="text-xl flex justify-between">
                <span>Message</span>
            </CardTitle>

            <CardContent className="text-xl bg-muted rounded-md border border-input p-4 overflow-auto">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptate consectetur illo accusamus, officia
                et aperiam odit minima suscipit cumque repellendus ea perferendis hic voluptatum perspiciatis quaerat.
                Consectetur aspernatur repudiandae culpa? Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                Dolorum exercitationem, enim quam dolor sunt at consequuntur facilis nisi obcaecati quas facere fugiat,
                blanditiis, quae quis repudiandae eos accusamus dignissimos officiis.
            </CardContent>

            <CardAction className="flex flex-row justify-center gap-1 items-center w-full">
                <Textarea placeholder="Aa" className="max-h-10 text-xl bg-muted" />
                <ImageButton path={SendSVG} alt="send" className="size-9 hover:size-10 transition-all" />
            </CardAction>
        </Card>
    );
};

const FilterAndEdit = () => {
    const [currTab, setCurrTab] = useState<"filter" | "edit">("filter");

    const handleTabChange = (tab: "filter" | "edit") => {
        if (currTab !== tab) {
            setCurrTab(tab);
        }
    };

    return (
        <Card className="h-full bg-card gap-2 pb-0">
            <CardHeader className="h-auto flex flex-row items-center">
                {/* <CardAction className="h-full flex flex-row items-center"> */}
                <Button
                    variant="ghost"
                    className={`p-4 ${currTab === "filter" && "bg-primary hover:bg-primary"}`}
                    onClick={() => handleTabChange("filter")}
                >
                    <CardTitle className="text-foreground">
                        <span>Filter</span>
                    </CardTitle>
                </Button>
                <Separator orientation="vertical" />
                <Button
                    variant="ghost"
                    className={`p-4 ${currTab === "edit" && "bg-primary hover:bg-primary"}`}
                    onClick={() => handleTabChange("edit")}
                >
                    <CardTitle className="text-foreground">
                        <span>Edit</span>
                    </CardTitle>
                </Button>
            </CardHeader>

            <CardContent className="h-full">
                <CardAction className={`h-full w-full ${currTab !== "filter" && "hidden"}`}>
                    <FilterProvider>
                        <TableFilter hasPaddingTop={false} hasPaddingBot={false} hasBorder={false} />
                    </FilterProvider>
                </CardAction>
                <CardAction className={`h-full w-full ${currTab !== "edit" && "hidden"}`}>
                    <QuickEditSection hasPaddingTop={false} hasPaddingBot={false} hasBorder={false} />
                </CardAction>
            </CardContent>
        </Card>
    );
};

const Actions = ({ openedTicket, onActionExitClick }: ActionProps) => {
    return (
        <div className="h-[100vh] py-4 pr-4 flex flex-col gap-2">
            <div className="">
                <Header openedTicket={openedTicket} onActionExitClick={onActionExitClick} />
            </div>
            <div className="flex-1 min-h-0">
                <Message openedTicket={openedTicket} />
            </div>
            <div className="flex-1">
                <FilterAndEdit />
            </div>
        </div>
    );
};

const TicketsPage = () => {
    const [openedTicket, setOpenedTicket] = useState<TicketType | undefined>(undefined);

    const handleAction = (ticket: TicketType) => {
        if (ticket.id !== openedTicket?.id) {
            setOpenedTicket(ticket);
        } else {
            setOpenedTicket(undefined);
        }
    };

    const handleActionExit = () => {
        if (setOpenedTicket) setOpenedTicket(undefined);
    };

    return (
        <div className="h-[100vh] grid grid-cols-15 gap-4">
            <div className={`${openedTicket ? "col-span-10 py-4 pl-4" : "col-span-15 p-4"} overflow-auto`}>
                <TicketTable edit={true} variant="combo" onActionClick={handleAction} />
            </div>

            <div className={`${openedTicket ? "col-span-5" : "hidden"}`}>
                <Actions openedTicket={openedTicket} onActionExitClick={handleActionExit} />
            </div>
        </div>
    );
};

export default TicketsPage;
