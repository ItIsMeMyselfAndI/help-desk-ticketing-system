import React, { useCallback, useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LockKeyholeIcon, Trash2Icon, UploadIcon } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { useMatchSize } from "@/hooks/use-screen-size";
import { ButtonTab } from "@/components/ButtonTab";
import { useTab } from "@/hooks/use-tab";
import { useTickets } from "@/hooks/use-tickets";
import { Selector } from "@/components/Selector";
import { APP_MIN_HEIGHT, CATEGORIES, MAIN_MIN_WIDTH } from "@/data/constants";
import { Textarea } from "@/components/ui/textarea";
import type { TicketType } from "@/types";

type TicketFormProps = {
    ticketID: string;
    uploadedFiles: File[];
    setUploadedFiles: React.Dispatch<React.SetStateAction<File[]>>;
};

const TicketForm = ({ ticketID, uploadedFiles, setUploadedFiles }: TicketFormProps) => {
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
        setUploadedFiles([]);
    }, [setTitle, setCategory, setDescription, setUploadedFiles]);

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

type DropAreaProps = {
    handleFileUpload: (files: File[]) => void;
};

const DropArea = ({ handleFileUpload }: DropAreaProps) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const dropAreaRef = useRef<HTMLDivElement>(null);
    const [isInside, setIsInside] = useState<boolean>(false);

    const handleBrowseClick = () => {
        fileInputRef.current?.click();
    };

    const handleFilesSelected = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = e.target.files ? Array.from(e.target.files) : [];
        selectedFiles.forEach((file) => console.log("file:", file));
        handleFileUpload(selectedFiles);
    };

    const handleFileDragEnter = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsInside(true);
        console.log("enter");
    };

    const handleFileDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        console.log("over");
    };

    const handleFileDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        e.preventDefault();
        // ignore if in children
        if (!dropAreaRef.current?.contains(e.relatedTarget as Node)) {
            setIsInside(false);
            console.log("leave");
        }
    };

    const handleFileDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.preventDefault();
        setIsInside(false);
        console.log("drop");

        const droppedFiles = Array.from(e.dataTransfer.files);
        droppedFiles.forEach((file) => console.log(file));
        handleFileUpload(droppedFiles);
    };

    return (
        <>
            <Card className="flex-1 p-14">
                <div
                    ref={dropAreaRef}
                    onDragEnter={handleFileDragEnter}
                    onDragOver={handleFileDragOver}
                    onDragLeave={handleFileDragLeave}
                    onDrop={handleFileDrop}
                    className={`flex-1 flex flex-col justify-center items-center gap-2 p-4 rounded-xl outline-4 outline-primary outline-dashed ${
                        isInside && "bg-muted opacity-50"
                    }`}
                >
                    <span className="text-primary text-2xl text-center font-semibold">Drag & Drop</span>
                    <UploadIcon className="size-12 text-primary" strokeWidth={2} />
                    {/* file uploads */}
                    <input
                        ref={fileInputRef}
                        type="file"
                        multiple
                        onChange={handleFilesSelected}
                        className="hidden"
                    ></input>
                    <Button
                        onClick={handleBrowseClick}
                        className={`h-auto bg-primary rounded-full px-6 hover:opacity-80`}
                    >
                        <span className={`whitespace-break-spaces text-xl font-semibold  text-foreground`}>
                            Browse Files
                        </span>
                    </Button>
                </div>
            </Card>
        </>
    );
};

type UploadedFilesProps = {
    uploadedFiles: File[];
    handleFileDelete: (file: File) => void;
};

const UploadedFiles = ({ uploadedFiles, handleFileDelete }: UploadedFilesProps) => {
    return (
        <>
            <Card className="min-h-0 flex-1 h-full flex flex-col gap-0 p-0">
                <CardTitle className="flex justify-start p-4">
                    <span className="text-primary text-xl">Uploaded Files</span>
                </CardTitle>
                <Separator orientation="horizontal" />
                <CardContent className="min-h-0 p-4 flex">
                    <div className="flex-1 overflow-y-auto flex flex-col gap-2">
                        {uploadedFiles.length === 0 ? (
                            <section className="h-full flex justify-center items-center">
                                <span>No files yet</span>
                            </section>
                        ) : (
                            uploadedFiles.map((file) => (
                                <div key={file.name} className="flex items-center gap-2">
                                    <div className="flex-1 min-w-0 flex py-2 px-4 rounded-xl border border-accent bg-muted">
                                        <section className="h-auto overflow-x-auto flex flex-row justify-start items-center">
                                            <span className="whitespace-nowrap text-foreground text-[1.1rem] font-normal">
                                                {file.name}
                                            </span>
                                        </section>
                                    </div>
                                    <Button
                                        onClick={() => handleFileDelete(file)}
                                        className="size-auto rounded-xl p-3 bg-red-500 hover:p-4 hover:bg-red-500"
                                    >
                                        <Trash2Icon className="size-5 text-foreground m-0 p-0" />
                                    </Button>
                                </div>
                            ))
                        )}
                    </div>
                </CardContent>
            </Card>
        </>
    );
};

const NewTicketPage = () => {
    const { origTickets } = useTickets();
    const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
    const isConstrainedWidth = useMatchSize("(max-width: 1160px");
    const { currTab, handleTabChange } = useTab("form");

    const getAvailableTicketID = () => {
        const lastID = origTickets[origTickets.length - 1].id;
        const idNumber = lastID.split("-")[1];
        return "TKT-" + String(Number(idNumber) + 1).padStart(3, "0");
    };

    const handleFileUpload = (files: File[]) => {
        console.log("\nOld");
        uploadedFiles.forEach((file) => console.log(file.name));

        const newFiles: File[] = [];
        const duplicateFiles: string[] = [];
        files.forEach((file) => {
            if (uploadedFiles.some((f) => file.name === f.name)) {
                duplicateFiles.push(file.name);
            } else {
                newFiles.push(file);
            }
        });
        setUploadedFiles((prev) => [...prev, ...newFiles]);

        console.log("\nNew");
        newFiles.forEach((file) => console.log(file.name));

        if (duplicateFiles.length !== 0) {
            let message = "The following files are already uploaded:";
            duplicateFiles.forEach((filename) => (message += "\n-\t" + filename));
            window.alert(message);
        }
    };

    const handleFileDelete = (file: File) => {
        const updatedFiles = uploadedFiles.filter((f: File) => f.name !== file.name);
        setUploadedFiles(updatedFiles);
    };

    return (
        <main
            className="h-[100vh] min-h-0 w-full flex flex-row gap-4 p-4"
            style={{ minHeight: APP_MIN_HEIGHT, minWidth: MAIN_MIN_WIDTH }}
        >
            {isConstrainedWidth ? (
                <div className="min-w-0 min-h-0 flex-1 flex flex-col gap-2">
                    {/* tabs */}
                    <section className="h-auto flex flex-row justify-end gap-2">
                        <ButtonTab tab="form" currTab={currTab} handleTabChange={handleTabChange} />
                        {/* <Separator orientation="vertical" /> */}
                        <ButtonTab tab="upload" currTab={currTab} handleTabChange={handleTabChange} />
                    </section>

                    {/* main */}
                    {currTab === "form" ? (
                        <section className="flex-1 min-h-0">
                            <TicketForm
                                uploadedFiles={uploadedFiles}
                                setUploadedFiles={setUploadedFiles}
                                ticketID={getAvailableTicketID()}
                            />
                        </section>
                    ) : (
                        <aside className="flex-1 flex flex-col gap-4">
                            <DropArea handleFileUpload={handleFileUpload} />
                            <UploadedFiles uploadedFiles={uploadedFiles} handleFileDelete={handleFileDelete} />
                        </aside>
                    )}
                </div>
            ) : (
                <>
                    <section className="flex-8">
                        <TicketForm
                            uploadedFiles={uploadedFiles}
                            setUploadedFiles={setUploadedFiles}
                            ticketID={getAvailableTicketID()}
                        />
                    </section>
                    <aside className="flex-5 min-w-0 max-w-lg flex flex-col gap-4">
                        <DropArea handleFileUpload={handleFileUpload} />
                        <UploadedFiles uploadedFiles={uploadedFiles} handleFileDelete={handleFileDelete} />
                    </aside>
                </>
            )}
        </main>
    );
};

export default NewTicketPage;
