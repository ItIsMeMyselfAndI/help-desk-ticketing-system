import { useRef, useState } from "react";
import { Card } from "./ui/card";
import { UploadIcon } from "lucide-react";
import { Button } from "./ui/button";

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

export { DropArea };
