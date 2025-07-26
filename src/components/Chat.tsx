import { Textarea } from "@/components/ui/textarea";
import SendSVG from "@/assets/send-svgrepo-com.svg";
import ProfileSVG from "@/assets/user-person-profile-block-account-circle-svgrepo-com.svg";
import { Card, CardAction, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ImageButton } from "@/components/ImageButton";
import { useTickets } from "@/hooks/use-tickets";
import chatHistorySample from "@/data/chat.sample.json";
import type { ChatType } from "@/types";
import { useEffect, useMemo, useState } from "react";

type ChatProps = {
    padding?: string;
    hasBorder?: boolean;
};

const Chat = ({ padding, hasBorder = true }: ChatProps) => {
    const { openedActionTicket } = useTickets();
    const [chatHistory, setChatHistory] = useState<ChatType[]>(chatHistorySample as ChatType[]);
    const [newMessage, setNewMessage] = useState<string>("");
    const newDateOBJ = new Date();

    useEffect(() => {
        if (openedActionTicket?.id === "") {
            setChatHistory([]);
        } else {
            setChatHistory(chatHistorySample as ChatType[]);
        }
    }, [openedActionTicket]);

    const renderedReversedChatHistory = useMemo(() => {
        const renderedElements = [];
        for (let i = chatHistory.length - 1; i >= 0; i--) {
            renderedElements.push(
                <div
                    key={i}
                    className={`flex flex-row ${
                        chatHistory[i].source === "you" ? "justify-end text-right" : "justify-start text-left"
                    }`}
                >
                    <div className="max-w-[70%] size-auto space-y-2">
                        <div
                            className={`rounded-3xl py-2 px-4 bg-accent whitespace-pre-wrap ${
                                chatHistory[i].source === "you" ? "bg-primary" : "bg-accent"
                            }`}
                        >
                            <span className="text-lg">{chatHistory[i].message}</span>
                        </div>
                        <p className="text-sm">{chatHistory[i].date}</p>
                    </div>
                </div>
            );
        }
        return renderedElements;
    }, [chatHistory]);

    const handleNewMessageSend = () => {
        if (!newMessage) return;
        const chat: ChatType = {
            source: "you",
            date: newDateOBJ.toISOString(),
            message: newMessage,
        };
        setChatHistory((prev) => [...prev, chat]);
        setNewMessage("");
    };

    const handleTextAreaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setNewMessage(e.target.value);
    };

    const handleTextAreaKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        // shift+enter => ignore = add new line
        if (e.key === "Enter" && e.shiftKey) {
            return;
        }
        // ctrl+enter => send
        else if (e.key === "Enter" && e.ctrlKey) {
            e.preventDefault();
            handleNewMessageSend();
        }
        // ctrl+enter => send
        else if (e.key === "Enter") {
            e.preventDefault();
            handleNewMessageSend();
        }
    };

    return (
        <Card className={`size-full text-xl flex flex-col gap-3 ${padding || "p-4"} ${!hasBorder && "border-none"}`}>
            <CardHeader className="text-xl flex justify-start gap-2 items-center px-0">
                <div className="size-auto rounded-full bg-white">
                    <img src={ProfileSVG} alt="" className="size-10" />
                </div>
                <CardTitle className="text-left">
                    <h3>{openedActionTicket?.assignedTo.name}</h3>
                    <span className="text-primary text-sm">{openedActionTicket?.assignedTo.role}</span>
                </CardTitle>
            </CardHeader>

            <CardContent className="flex-1 flex flex-col-reverse overflow-auto gap-4 text-xl bg-muted rounded-md border border-input p-4">
                {renderedReversedChatHistory}
            </CardContent>

            <CardAction className="flex flex-row justify-center gap-1 items-center w-full">
                <Textarea
                    value={newMessage}
                    onChange={handleTextAreaChange}
                    onKeyDown={handleTextAreaKeyDown}
                    placeholder="Aa"
                    className="max-h-10 text-xl bg-muted"
                />
                <ImageButton
                    path={SendSVG}
                    alt="send"
                    className="size-9 hover:size-10 transition-all"
                    onClick={handleNewMessageSend}
                />
            </CardAction>
        </Card>
    );
};

export { Chat };
