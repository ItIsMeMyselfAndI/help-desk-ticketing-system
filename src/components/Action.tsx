import { useEffect, useState } from "react";
import { Card, CardAction, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { selectStatusBGColor } from "@/lib/utils";
import { ImageButton } from "@/components/ImageButton";
import { FilterProvider } from "@/contexts/FilterContext";
import { Separator } from "@/components/ui/separator";
import { TableFilter } from "@/components/TableFIlter";
import { QuickEdit } from "@/components/QuickEdit";
import XCloseSVG from "@/assets/close-circle-svgrepo-com.svg";
import { Chat } from "@/components/Chat";
import { TicketDetails } from "./TicketDetails";
import { useTickets } from "@/hooks/use-tickets";
import type { ActionTabType } from "@/types";
import { ButtonTab } from "./ButtonTab";
import { useCustomScreenSize } from "@/hooks/use-screen-size";
import { APP_MIN_HEIGHT } from "@/data/constants";

type ActionsProps = {
    variant?: "default" | "full";
    onActionsExitClick?: () => void;
};

const ActionHeader = ({ onActionsExitClick }: ActionsProps) => {
    const { openedActionTicket } = useTickets();

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

type FullActionsProps = {
    onActionsExitClick?: () => void;
};

const FullActions = ({ onActionsExitClick }: FullActionsProps) => {
    const isConstrainedSize = useCustomScreenSize("(max-height: 890px)");
    const [currTab, setCurrTab] = useState<ActionTabType>("details");

    const handleTabChange = (tab: ActionTabType) => {
        if (currTab !== tab) {
            setCurrTab(tab);
        }
    };

    useEffect(() => {
        if (isConstrainedSize) {
            if (currTab === "others") {
                setCurrTab("filter");
            }
        } else {
            if (["filter", "edit"].includes(currTab)) {
                setCurrTab("others");
            }
        }
    }, [currTab, setCurrTab, isConstrainedSize]);

    return (
        <div className={`h-[100vh] flex flex-col gap-2 p-4 xl:pl-0`} style={{ minHeight: APP_MIN_HEIGHT }}>
            <div>
                <ActionHeader onActionsExitClick={onActionsExitClick} />
            </div>
            <div className="flex-1 space-2 min-h-0">
                <Card className="h-full bg-card gap-0 p-0">
                    <CardHeader className="h-auto flex flex-row justify-end items-center p-2">
                        <ButtonTab tab="details" currTab={currTab} handleTabChange={handleTabChange} />
                        <Separator orientation="vertical" />
                        <ButtonTab tab="chat" currTab={currTab} handleTabChange={handleTabChange} />
                        <Separator orientation="vertical" />
                        {isConstrainedSize ? (
                            <>
                                <ButtonTab tab="filter" currTab={currTab} handleTabChange={handleTabChange} />
                                <Separator orientation="vertical" />
                                <ButtonTab tab="edit" currTab={currTab} handleTabChange={handleTabChange} />
                            </>
                        ) : (
                            <ButtonTab tab="others" currTab={currTab} handleTabChange={handleTabChange} />
                        )}
                    </CardHeader>

                    <Separator orientation="horizontal" />

                    <CardContent className="flex-1 min-h-0 p-4">
                        {/* ticket details */}
                        <CardAction className={`size-full ${currTab !== "details" && "hidden"}`}>
                            <TicketDetails hasBorder={true} />
                        </CardAction>
                        {/* chat */}
                        <CardAction className={`size-full ${currTab !== "chat" && "hidden"}`}>
                            <Chat padding="p-0" hasBorder={false} />
                        </CardAction>
                        {/* filter & edit */}
                        {isConstrainedSize ? (
                            <>
                                <CardAction className={`size-full ${currTab !== "filter" && "hidden"}`}>
                                    <FilterProvider>
                                        <TableFilter />
                                    </FilterProvider>
                                </CardAction>
                                <CardAction className={`size-full ${currTab !== "edit" && "hidden"}`}>
                                    <QuickEdit />
                                </CardAction>
                            </>
                        ) : (
                            <CardAction className={`size-full ${currTab !== "others" && "hidden"}`}>
                                <div className="flex flex-col gap-4">
                                    <FilterProvider>
                                        <TableFilter variant="full" />
                                    </FilterProvider>
                                    <QuickEdit />
                                </div>
                            </CardAction>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

const DefaultActions = () => {
    const isConstrainedSize = useCustomScreenSize("(max-height: 890px)");
    const [currTab, setCurrTab] = useState<ActionTabType>("filter");

    const handleTabChange = (tab: ActionTabType) => {
        if (currTab !== tab) {
            setCurrTab(tab);
        }
    };

    return isConstrainedSize ? (
        <Card className="h-full bg-card gap-0 p-0">
            <CardHeader className="h-auto flex flex-row justify-end items-center p-2">
                <ButtonTab tab="filter" currTab={currTab} handleTabChange={handleTabChange} />
                <Separator orientation="vertical" />
                <ButtonTab tab="edit" currTab={currTab} handleTabChange={handleTabChange} />
            </CardHeader>

            <Separator orientation="horizontal" />

            <CardContent className="flex-1 min-h-0 p-4">
                {/* filter */}
                <CardAction className={`size-full ${currTab !== "filter" && "hidden"}`}>
                    <FilterProvider>
                        <TableFilter />
                    </FilterProvider>
                </CardAction>
                {/* edit */}
                <CardAction className={`size-full ${currTab !== "edit" && "hidden"}`}>
                    <QuickEdit />
                </CardAction>
            </CardContent>
        </Card>
    ) : (
        <div className="h-full flex flex-col gap-4">
            <section className="flex-1">
                <FilterProvider>
                    <TableFilter variant="full" />
                </FilterProvider>
            </section>
            <section className="flex-1">
                <QuickEdit />
            </section>
        </div>
    );
};

const Actions = ({ variant = "default", onActionsExitClick }: ActionsProps) => {
    return variant === "full" ? <FullActions onActionsExitClick={onActionsExitClick} /> : <DefaultActions />;
};

export { Actions };
