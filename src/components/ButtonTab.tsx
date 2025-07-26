import type { ActionTabType } from "@/types";
import { Button } from "./ui/button";
import { CardTitle } from "./ui/card";

type ButtonTabProp = {
    tab: ActionTabType;
    currTab: ActionTabType;
    handleTabChange: (tab: ActionTabType) => void;
};

const ButtonTab = ({ tab, currTab, handleTabChange }: ButtonTabProp) => {
    return (
        <Button
            variant="ghost"
            className={`p-4 ${currTab === tab && "bg-primary hover:bg-primary"}`}
            onClick={() => handleTabChange(tab)}
        >
            <CardTitle className="text-foreground">
                <span>{tab[0].toUpperCase() + tab.slice(1)}</span>
            </CardTitle>
        </Button>
    );
};

export { ButtonTab };
