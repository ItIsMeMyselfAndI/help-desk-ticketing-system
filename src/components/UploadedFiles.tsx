import { Trash2Icon } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent, CardTitle } from "./ui/card";
import { Separator } from "./ui/separator";

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

export { UploadedFiles };
