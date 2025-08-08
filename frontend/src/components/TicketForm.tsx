import { Selector } from "@/components/Selector";
import { Textarea } from "@/components/ui/textarea";
import { useMatchSize } from "@/hooks/use-screen-size";
import { useTickets } from "@/hooks/use-tickets";
import type { TicketType } from "@/types";
import { useCallback, useEffect, useState } from "react";
import { Card, CardHeader } from "./ui/card";
import { LockKeyholeIcon } from "lucide-react";
import { CATEGORIES } from "@/data/constants";
import { Button } from "./ui/button";
import { Separator } from "./ui/separator";

type TicketFormProps = {
    ticketID: string;
    uploadedFiles: File[];
    setAttachments: React.Dispatch<React.SetStateAction<File[]>>;
};

const TicketForm = ({ ticketID, uploadedFiles, setAttachments }: TicketFormProps) => {
    const defaultStatus = "Open";
    const defaultCategory = "None";
    const { origTickets, setOrigTickets } = useTickets();
    const isConstrainedSize = useMatchSize("(max-width: 500px)");
    const date = new Date();
    // new ticket
    const [newTicket, setNewTicket] = useState<TicketType | null>(null);
    const [title, setTitle] = useState<string>("");
    const [category, setCategory] = useState<string>(defaultCategory);
    const [description, setDescription] = useState<string>("");
    const currDate = date.toISOString().split("T")[0];

    const handleTitle = (e: React.ChangeEvent<HTMLInputElement>) => setTitle(e.target.value);
    const handleCategory = (value: string) => setCategory(value);
    const handleDescription = (e: React.ChangeEvent<HTMLTextAreaElement>) => setDescription(e.target.value);

    useEffect(() => {
        setNewTicket(() => {
            return {
                id: ticketID,
                title: title,
                status: defaultStatus,
                category: category,
                description: description,
                files: uploadedFiles,
                createdAt: currDate,
                updatedAt: currDate,
                assignedTo: null,
            } as TicketType;
        });
    }, [ticketID, title, category, description, uploadedFiles, currDate, setNewTicket]);

    const _resetStates = useCallback(() => {
        setNewTicket(null);
        setTitle("");
        setCategory(defaultCategory);
        setDescription("");
        setAttachments([]);
    }, [setTitle, setCategory, setDescription, setAttachments]);

    const handleSubmit = (e: React.MouseEvent) => {
        e.preventDefault();
        if (title === "") {
            window.alert("Please enter a title");
            return;
        } else if (category === defaultCategory) {
            window.alert("Please choose a category");
            return;
        } else if (description === "") {
            window.alert("Please write a short description");
            return;
        } else if (newTicket !== null) {
            setOrigTickets((prev) => [...prev, newTicket]);
            console.log("submitted:", newTicket);
            console.log("first:", origTickets[0]);
            _resetStates();
        }
    };

    const handleReset = () => {
        if (newTicket !== null) {
            _resetStates();
        }
    };

    return (
        <Card className="flex-1 size-full min-h-0 text-2xl text-foreground/80 flex flex-col gap-2 p-0 border-none rounded-none bg-transparent">
            <CardHeader className="p-0">
                <span className="text-5xl text-primary font-bold p-0">{ticketID}</span>
            </CardHeader>

            <div className="flex size-full min-h-0 p-6 rounded-xl border border-border bg-card">
                <form className="flex-1 overflow-auto flex flex-col gap-4 bg-transparent">
                    <section className="flex flex-col gap-4">
                        <label htmlFor="title" className="font-semibold">
                            Title
                        </label>
                        <input
                            id="title"
                            type="text"
                            value={title}
                            onChange={handleTitle}
                            className="border border-input rounded-xl py-2 px-4 bg-muted"
                        />
                    </section>

                    <section className="flex flex-row gap-4">
                        <div className="flex-1 flex flex-col gap-4">
                            <label htmlFor="status" className="font-semibold">
                                Status
                            </label>
                            <div className="flex flex-row justify-between items-center border border-input rounded-xl py-2 px-4 bg-background hover:cursor-not-allowed">
                                <span id="status" className="text-2xl">
                                    Open
                                </span>
                                <LockKeyholeIcon className="size-10 text-foreground p-2 rounded-xl bg-orange-500" />
                            </div>
                        </div>
                        <div className="flex-1 flex flex-col gap-4">
                            <label htmlFor="category" className="font-semibold">
                                Category
                            </label>
                            <Selector
                                id="category"
                                options={CATEGORIES}
                                defaultItem={defaultCategory}
                                selectedItem={category}
                                handleSelectionChange={handleCategory}
                            />
                        </div>
                    </section>

                    <section className="flex-1 flex flex-col gap-4">
                        <label htmlFor="description" className="font-semibold">
                            Description
                        </label>
                        <Textarea
                            id="description"
                            value={description}
                            onChange={handleDescription}
                            className="flex-1 text-2xl border border-input rounded-xl py-2 px-4 bg-muted"
                        />
                    </section>

                    <section className={`flex gap-4 ${isConstrainedSize ? "flex-col" : "flex-row"}`}>
                        <div className="flex-1 flex flex-col gap-4">
                            <label className="font-semibold">Created at</label>
                            <div className="flex flex-row justify-between items-center border border-input rounded-xl py-2 px-4 bg-background hover:cursor-not-allowed">
                                <span className="text-2xl">{date.toISOString().split("T")[0]}</span>
                                <LockKeyholeIcon className="size-10 text-foreground p-2 rounded-xl bg-orange-500" />
                            </div>
                        </div>
                        <div className="flex-1 flex flex-col gap-4">
                            <label className="font-semibold">Updated at</label>
                            <div className="flex flex-row justify-between items-center border border-input rounded-xl py-2 px-4 bg-background hover:cursor-not-allowed">
                                <span className="text-2xl">{date.toISOString().split("T")[0]}</span>
                                <LockKeyholeIcon className="size-10 text-foreground p-2 rounded-xl bg-orange-500" />
                            </div>
                        </div>
                    </section>

                    <section className="flex flex-col gap-4">
                        <label className="font-semibold">Assigned to</label>
                        <div className="flex flex-row justify-between items-center border border-input rounded-xl py-2 px-4 bg-background hover:cursor-not-allowed">
                            <span className="text-2xl">To be assigned</span>
                            <LockKeyholeIcon className="size-10 text-foreground p-2 rounded-xl bg-orange-500" />
                        </div>
                    </section>

                    <Separator orientation="horizontal" />

                    <section className="flex flex-row justify-end items-center gap-4">
                        <Button
                            type="submit"
                            onClick={handleSubmit}
                            className="p-6 rounded-xl bg-yellow-500 hover:bg-yellow-500 hover:p-7"
                        >
                            <span className="text-2xl font-semibold text-foreground/80">Submit</span>
                        </Button>
                        <Button
                            type="reset"
                            onClick={handleReset}
                            className="p-6 rounded-xl bg-red-500 hover:bg-red-500 hover:p-7"
                        >
                            <span className="text-2xl font-semibold text-foreground/80">Reset</span>
                        </Button>
                    </section>
                </form>
            </div>
        </Card>
    );
};

export { TicketForm };
