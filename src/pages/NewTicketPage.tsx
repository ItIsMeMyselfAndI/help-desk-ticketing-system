import React, { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { UploadIcon } from "lucide-react";

type DropAreaProps = {
    updateFiles: (files: File[]) => void;
};

const DropArea = ({ updateFiles }: DropAreaProps) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const dropAreaRef = useRef<HTMLDivElement>(null);
    const [isInside, setIsInside] = useState<boolean>(false);

    const handleBrowseClick = () => {
        fileInputRef.current?.click();
    };

    const handleFilesSelected = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = e.target.files ? Array.from(e.target.files) : [];
        selectedFiles.forEach((file) => console.log("file:", file));
        updateFiles(selectedFiles);
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
        updateFiles(droppedFiles);
    };

    return (
        <>
            <Card className="flex-3 p-14">
                <div
                    ref={dropAreaRef}
                    onDragEnter={handleFileDragEnter}
                    onDragOver={handleFileDragOver}
                    onDragLeave={handleFileDragLeave}
                    onDrop={handleFileDrop}
                    className={`flex-1 flex flex-col justify-center items-center gap-2 rounded-xl outline-4 outline-primary outline-dashed ${
                        isInside && "bg-muted"
                    }`}
                >
                    <span className="text-primary text-2xl">Drag & Drop Files</span>
                    <UploadIcon className="size-12 text-primary" strokeWidth={2} />
                    {/* file uploads */}
                    <input
                        ref={fileInputRef}
                        type="file"
                        multiple
                        onChange={handleFilesSelected}
                        className="hidden"
                    ></input>
                    <Button onClick={handleBrowseClick} className="text-foreground rounded-full px-6">
                        <span className="text-foreground text-xl">Browse Files</span>
                    </Button>
                </div>
            </Card>
        </>
    );
};

const UploadedFiles = () => {
    return (
        <>
            <Card className="flex-2"></Card>
        </>
    );
};

const NewTicketPage = () => {
    const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

    const updateFiles = (files: File[]) => {
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

    return (
        <main className="h-[100vh] w-full flex flex-row gap-4 p-4">
            <form className="flex-8">
                <Card className="size-full"></Card>
            </form>
            <aside className="flex-5 max-w-lg flex flex-col gap-4">
                <DropArea updateFiles={updateFiles} />
                <UploadedFiles />
            </aside>
        </main>
    );
};

export default NewTicketPage;
