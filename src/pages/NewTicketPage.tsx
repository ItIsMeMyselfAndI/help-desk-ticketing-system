import React, { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
import { Trash2Icon, UploadIcon } from "lucide-react";
import { Separator } from "@/components/ui/separator";

type DropAreaProps = {
    handleAddNewFiles: (files: File[]) => void;
};

const DropArea = ({ handleAddNewFiles }: DropAreaProps) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const dropAreaRef = useRef<HTMLDivElement>(null);
    const [isInside, setIsInside] = useState<boolean>(false);

    const handleBrowseClick = () => {
        fileInputRef.current?.click();
    };

    const handleFilesSelected = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = e.target.files ? Array.from(e.target.files) : [];
        selectedFiles.forEach((file) => console.log("file:", file));
        handleAddNewFiles(selectedFiles);
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
        handleAddNewFiles(droppedFiles);
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
                    <span className="text-primary text-2xl font-semibold">Drag & Drop</span>
                    <UploadIcon className="size-12 text-primary" strokeWidth={2} />
                    {/* file uploads */}
                    <input
                        ref={fileInputRef}
                        type="file"
                        multiple
                        onChange={handleFilesSelected}
                        className="hidden"
                    ></input>
                    <Button onClick={handleBrowseClick} className={`bg-primary rounded-full px-6 hover:opacity-80`}>
                        <span className={`text-xl font-semibold text-foreground`}>Browse Files</span>
                    </Button>
                </div>
            </Card>
        </>
    );
};

type UploadedFilesProps = {
    uploadedFiles: File[];
    handleDeleteFile: (file: File) => void;
};

const UploadedFiles = ({ uploadedFiles, handleDeleteFile }: UploadedFilesProps) => {
    return (
        <>
            <Card className="flex-1 flex flex-col gap-0 p-0 min-h-0">
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
                                        <section className="h-auto overflow-x-auto flex flex-row justify-center items-center">
                                            <span className="whitespace-nowrap text-foreground text-lg font-normal">
                                                {file.name}
                                            </span>
                                        </section>
                                    </div>
                                    <Button
                                        onClick={() => handleDeleteFile(file)}
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
    const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

    const handleAddNewFiles = (files: File[]) => {
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

    const handleDeleteFile = (file: File) => {
        const updatedFiles = uploadedFiles.filter((f: File) => f.name !== file.name);
        setUploadedFiles(updatedFiles);
    };

    return (
        <main className="h-[100vh] w-full flex flex-row gap-4 p-4">
            <form className="flex-8">
                <Card className="size-full"></Card>
            </form>
            <aside className="flex-5 min-w-0 max-w-lg flex flex-col gap-4">
                <DropArea handleAddNewFiles={handleAddNewFiles} />
                <UploadedFiles uploadedFiles={uploadedFiles} handleDeleteFile={handleDeleteFile} />
            </aside>
        </main>
    );
};

export default NewTicketPage;
