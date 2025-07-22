import { Textarea } from "@/components/ui/textarea";
import SendSVG from "@/assets/send-svgrepo-com.svg";
import ProfileSVG from "@/assets/user-person-profile-block-account-circle-svgrepo-com.svg";
import type { TicketType } from "@/types";
import { Card, CardAction, CardContent, CardHeader, CardTitle } from "./ui/card";
import { ImageButton } from "./ImageButton";

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

export { Chat };
