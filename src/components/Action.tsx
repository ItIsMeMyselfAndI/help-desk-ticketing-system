import { useState } from "react";
import { Card, CardAction, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { selectStatusBGColor } from "@/lib/utils";
import { ImageButton } from "@/components/ImageButton";
import SendSVG from "@/assets/send-svgrepo-com.svg";
import { Button } from "@/components/ui/button";
import { FilterProvider } from "@/contexts/FilterContext";
import { Separator } from "@/components/ui/separator";
import { TableFilter } from "@/components/TableFIlter";
import { QuickEdit } from "@/components/QuickEdit";
import type { TicketType } from "@/types";
import XCloseSVG from "@/assets/close-circle-svgrepo-com.svg";
import ProfileSVG from "@/assets/user-person-profile-block-account-circle-svgrepo-com.svg";

type ActionsProps = {
    openedTicket: TicketType | undefined;
    onActionsExitClick?: () => void;
};

const Header = ({ openedTicket, onActionsExitClick }: ActionsProps) => {
    return (
        <CardHeader className="flex flex-row justify-between p-0">
            <section className="flex flex-row gap-2 items-center">
                <CardTitle className="text-primary text-2xl">Actions</CardTitle>
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
            <ImageButton
                path={XCloseSVG}
                alt="X"
                className="size-9 hover:size-10 transition-all"
                onClick={onActionsExitClick}
            />
        </CardHeader>
    );
};

const TicketDetails = ({ openedTicket }: { openedTicket: TicketType | undefined }) => {
    return (
        <Card className="h-full">
            <CardTitle>
                <span className="text-primary">Details</span>
            </CardTitle>
        </Card>
    );
};

type ChatProps = {
    openedTicket: TicketType | undefined;
    padding?: string;
    hasBorder?: boolean;
};

const Chat = ({ openedTicket, padding, hasBorder = true }: ChatProps) => {
    return (
        <Card className={`size-full text-xl flex flex-col gap-3 ${padding || "p-4"} ${!hasBorder && "border-none"}`}>
            <CardHeader className="text-xl flex justify-start gap-2 items-center px-0">
                <div className="size-auto rounded-full bg-white">
                    <img src={ProfileSVG} alt="" className="size-10" />
                </div>
                <CardTitle className="text-right">
                    <h3>{openedTicket?.assigned_to.name}</h3>
                    <span className="text-primary text-sm">{openedTicket?.assigned_to.role}</span>
                </CardTitle>
            </CardHeader>

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

const DetailsAndChat = ({ openedTicket }: { openedTicket: TicketType | undefined }) => {
    const [currTab, setCurrTab] = useState<"details" | "chat">("details");

    const handleTabChange = (tab: "details" | "chat") => {
        if (currTab !== tab) {
            setCurrTab(tab);
        }
    };

    return (
        <Card className="h-full bg-card gap-0 p-0">
            <CardHeader className="h-auto flex flex-row justify-end items-center p-2">
                <Button
                    variant="ghost"
                    className={`p-4 ${currTab === "details" && "bg-primary hover:bg-primary"}`}
                    onClick={() => handleTabChange("details")}
                >
                    <CardTitle className="text-foreground">
                        <span>Details</span>
                    </CardTitle>
                </Button>
                <Separator orientation="vertical" />
                <Button
                    variant="ghost"
                    className={`p-4 ${currTab === "chat" && "bg-primary hover:bg-primary"}`}
                    onClick={() => handleTabChange("chat")}
                >
                    <CardTitle className="text-foreground">
                        <span>Chat</span>
                    </CardTitle>
                </Button>
            </CardHeader>

            <Separator orientation="horizontal" />

            <CardContent className="flex-1 min-h-0 p-4">
                <CardAction className={`size-full ${currTab !== "details" && "hidden"}`}>
                    <TicketDetails openedTicket={openedTicket} />
                </CardAction>
                <CardAction className={`size-full ${currTab !== "chat" && "hidden"}`}>
                    <Chat openedTicket={openedTicket} padding="p-0" hasBorder={false} />
                </CardAction>
            </CardContent>
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
        <Card className="h-full bg-card gap-0 p-0">
            <CardHeader className="h-auto flex flex-row justify-start items-center p-2">
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

            <Separator orientation="horizontal" />

            <CardContent className="flex-1 p-4">
                <CardAction className={`size-full ${currTab !== "filter" && "hidden"}`}>
                    <FilterProvider>
                        <TableFilter padding="py-0" hasBorder={false} />
                    </FilterProvider>
                </CardAction>
                <CardAction className={`size-full ${currTab !== "edit" && "hidden"}`}>
                    <QuickEdit padding="py-0" hasBorder={false} />
                </CardAction>
            </CardContent>
        </Card>
    );
};

const Actions = ({ openedTicket, onActionsExitClick }: ActionsProps) => {
    return (
        <div className="h-[100vh] py-4 pr-4 flex flex-col gap-2">
            <div className="">
                <Header openedTicket={openedTicket} onActionsExitClick={onActionsExitClick} />
            </div>
            <div className="flex-1 grid grid-rows-13 gap-2 min-h-0">
                <div className="row-span-7 min-h-0">
                    <DetailsAndChat openedTicket={openedTicket} />
                </div>
                <div className="row-span-6">
                    <FilterAndEdit />
                </div>
            </div>
        </div>
    );
};

export { Actions };
