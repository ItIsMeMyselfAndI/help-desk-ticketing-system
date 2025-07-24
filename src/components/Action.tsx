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
import type { ActionTabType } from "@/types";

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

type ButtonTabProp = {
    tab: ActionTabType;
    currTab: ActionTabType;
    handleTabChange: (tab: ActionTabType) => void;
};

const ButtonTab = ({ tab, currTab, handleTabChange }: ButtonTabProp) => {
    return (
        <Button
            variant="ghost"
            className={`p-4 ${currTab === tab && "bg-primary hover:bg-primary"}`}
            onClick={() => handleTabChange(tab)}
        >
            <CardTitle className="text-foreground">
                <span>{tab[0].toUpperCase() + tab.slice(1)}</span>
            </CardTitle>
        </Button>
    );
};

const Actions = ({ onActionsExitClick }: ActionsProps) => {
    const [currTab, setCurrTab] = useState<ActionTabType>("details");

    const handleTabChange = (tab: ActionTabType) => {
        if (currTab !== tab) {
            setCurrTab(tab);
        }
    };

    return (
        <div className="h-[100vh] flex flex-col gap-2 p-4 xl:pl-0">
            <div className="">
                <Header onActionsExitClick={onActionsExitClick} />
            </div>
            <div className="flex-1 space-2 min-h-0">
                <Card className="h-full bg-card gap-0 p-0">
                    <CardHeader className="h-auto flex flex-row justify-end items-center p-2">
                        <ButtonTab tab="details" currTab={currTab} handleTabChange={handleTabChange} />
                        <Separator orientation="vertical" />
                        <ButtonTab tab="chat" currTab={currTab} handleTabChange={handleTabChange} />
                        <Separator orientation="vertical" />
                        <ButtonTab tab="others" currTab={currTab} handleTabChange={handleTabChange} />
                    </CardHeader>

                    <Separator orientation="horizontal" />

                    <CardContent className="flex-1 min-h-0 p-4">
                        {/* ticket details */}
                        <CardAction className={`size-full min-w-0 ${currTab !== "details" && "hidden"}`}>
                            <TicketDetails padding="p-2" hasBorder={false} />
                        </CardAction>
                        {/* chat */}
                        <CardAction className={`size-full ${currTab !== "chat" && "hidden"}`}>
                            <Chat padding="p-0" hasBorder={false} />
                        </CardAction>
                        {/* filter & edit */}
                        <CardAction className={`size-full ${currTab !== "others" && "hidden"}`}>
                            <div className="grid grid-rows-2 gap-4">
                                <div className="row-span-1">
                                    <FilterProvider>
                                        <TableFilter />
                                    </FilterProvider>
                                </div>
                                <div className="row-span-1">
                                    <QuickEdit />
                                </div>
                            </div>
                        </CardAction>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export { Actions };
