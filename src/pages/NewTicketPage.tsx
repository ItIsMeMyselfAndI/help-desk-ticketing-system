import { useState } from "react";
import { useMatchSize } from "@/hooks/use-screen-size";
import { ButtonTab } from "@/components/ButtonTab";
import { useTab } from "@/hooks/use-tab";
import { useTickets } from "@/hooks/use-tickets";
import { APP_MIN_HEIGHT, MAIN_MIN_WIDTH } from "@/data/constants";
import { TicketForm } from "@/components/TicketForm";
import { DropArea } from "@/components/DropArea";
import { Attachments } from "@/components/Attachments";

const NewTicketPage = () => {
    const { origTickets } = useTickets();
    const [uploadedFiles, setAttachments] = useState<File[]>([]);
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
        setAttachments((prev) => [...prev, ...newFiles]);

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
        setAttachments(updatedFiles);
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
                                setAttachments={setAttachments}
                                ticketID={getAvailableTicketID()}
                            />
                        </section>
                    ) : (
                        <aside className="flex-1 flex flex-col gap-4">
                            <DropArea handleFileUpload={handleFileUpload} />
                            <Attachments uploadedFiles={uploadedFiles} handleFileDelete={handleFileDelete} />
                        </aside>
                    )}
                </div>
            ) : (
                <>
                    <section className="flex-8">
                        <TicketForm
                            uploadedFiles={uploadedFiles}
                            setAttachments={setAttachments}
                            ticketID={getAvailableTicketID()}
                        />
                    </section>
                    <aside className="flex-5 min-w-0 max-w-lg flex flex-col gap-4">
                        <DropArea handleFileUpload={handleFileUpload} />
                        <Attachments uploadedFiles={uploadedFiles} handleFileDelete={handleFileDelete} />
                    </aside>
                </>
            )}
        </main>
    );
};

export default NewTicketPage;
