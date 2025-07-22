import { useState } from "react";
import { Card, CardAction, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { selectStatusBGColor } from "@/lib/utils";
import { ImageButton } from "@/components/ImageButton";
import { Button } from "@/components/ui/button";
import { FilterProvider } from "@/contexts/FilterContext";
import { Separator } from "@/components/ui/separator";
import { TableFilter } from "@/components/TableFIlter";
import { QuickEdit } from "@/components/QuickEdit";
import XCloseSVG from "@/assets/close-circle-svgrepo-com.svg";
import { Chat } from "@/components/Chat";
import { TicketDetails } from "./TicketDetails";
import { useTicketContext } from "@/contexts/TicketContext";

type ActionsProps = {
    onActionsExitClick?: () => void;
};

const Header = ({ onActionsExitClick }: ActionsProps) => {
    const { openedActionTicket } = useTicketContext();

    return (
        <CardHeader className="flex flex-row justify-between p-0">
            <section className="flex flex-row gap-2 items-center">
                <CardTitle className="text-primary text-2xl">Actions</CardTitle>
                <span className="text-lg">{openedActionTicket ? openedActionTicket.id : "None"}</span>
                {openedActionTicket ? (
                    <span
                        className={`${selectStatusBGColor(
                            openedActionTicket.status
                        )} font-normal py-1 px-2 rounded-xl text-center`}
                    >
                        {openedActionTicket.status}
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

const DetailsAndChat = () => {
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

            <CardContent className="flex-1 min-h-0 p-4 min-w-0 overflow-x-auto">
                <CardAction className={`size-full min-w-0 overflow-x-auto ${currTab !== "details" && "hidden"}`}>
                    <TicketDetails padding="p-2" hasBorder={false} />
                </CardAction>
                <CardAction className={`size-full ${currTab !== "chat" && "hidden"}`}>
                    <Chat padding="p-0" hasBorder={false} />
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

const Actions = ({ onActionsExitClick }: ActionsProps) => {
    return (
        <div className="h-[100vh] py-4 pr-4 flex flex-col gap-2">
            <div className="">
                <Header onActionsExitClick={onActionsExitClick} />
            </div>
            <div className="flex-1 grid grid-rows-13 gap-2 min-h-0">
                <div className="row-span-7 min-w-0">
                    <DetailsAndChat />
                </div>
                <div className="row-span-6">
                    <FilterAndEdit />
                </div>
            </div>
        </div>
    );
};

export { Actions };
