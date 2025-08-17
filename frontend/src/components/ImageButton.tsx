import React from "react";

type ImageButtonProp = {
    path: string;
    alt?: string;
    className?: string;
    onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
};

const ImageButton = ({ path, alt = "", className, onClick }: ImageButtonProp) => {
    return (
        <button
            className={`p-1 border-0 rounded-full bg-transparent active:bg-accent/50 ${className || ""}`}
            onClick={onClick}
            type="button"
        >
            <img src={path} alt={alt} className="w-full h-full" />
        </button>
    );
};

export { ImageButton };
