import { TicketTable } from "@/components/TicketTable";
import { Card, CardAction, CardContent, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { selectStatusBGColor } from "@/lib/utils";
import type { TicketType } from "@/types";
import { useState } from "react";
import CloseXSVG from "@/assets/close-circle-svgrepo-com.svg";
import { ImageButton } from "@/components/ImageButton";
import SendSVG from "@/assets/send-svgrepo-com.svg";

type ActionProps = {
    openedTicket: TicketType | undefined;
    setOpenedTicket?: React.Dispatch<React.SetStateAction<TicketType | undefined>>;
};

const ActionHeader = ({ openedTicket, setOpenedTicket }: ActionProps) => {
    const handleActionClose = () => {
        if (setOpenedTicket) setOpenedTicket(undefined);
    };

    return (
        <header className="text-2xl flex flex-col gap-1">
            <section className="flex flex-row justify-between items-center">
                <h3 className="text-primary">Actions</h3>
                <ImageButton
                    path={CloseXSVG}
                    alt="X"
                    className="size-9 hover:size-10 transition-all"
                    onClick={handleActionClose}
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

const MessageSection = ({ openedTicket }: ActionProps) => {
    return (
        <Card className="size-full p-4 text-xl bg-muted flex flex-col gap-3">
            {openedTicket && (
                <CardTitle className="text-xl flex justify-between">
                    <span>Messages</span>
                </CardTitle>
            )}

            <CardContent className="text-xl bg-card rounded-md border border-input p-4 overflow-auto">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptate consectetur illo accusamus, officia
                et aperiam odit minima suscipit cumque repellendus ea perferendis hic voluptatum perspiciatis quaerat.
                Consectetur aspernatur repudiandae culpa? Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                Dolorum exercitationem, enim quam dolor sunt at consequuntur facilis nisi obcaecati quas facere fugiat,
                blanditiis, quae quis repudiandae eos accusamus dignissimos officiis.
            </CardContent>

            <CardAction className="flex flex-row justify-center gap-1 items-center w-full">
                <Textarea placeholder="Aa" className="max-h-10 text-xl bg-card" />
                <ImageButton path={SendSVG} alt="send" className="size-9 hover:size-10 transition-all" />
            </CardAction>
        </Card>
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

    return (
        <div className="h-[100vh] p-4 grid grid-cols-15 gap-4">
            <div className={`${openedTicket ? "col-span-10" : "col-span-15"} overflow-auto`}>
                <TicketTable edit={true} variant="combo" onActionClick={handleAction} />
            </div>
            <div className={`flex flex-col gap-2 h-full ${openedTicket ? "col-span-5" : "hidden"}`}>
                <div className="mb-2">
                    <ActionHeader openedTicket={openedTicket} setOpenedTicket={setOpenedTicket} />
                </div>
                <div className="flex-1 min-h-0">
                    <MessageSection openedTicket={openedTicket} />
                </div>
                <div className="flex-1">
                    <Card className="h-full bg-muted"></Card>
                </div>
            </div>
        </div>
    );
};

export default TicketsPage;
