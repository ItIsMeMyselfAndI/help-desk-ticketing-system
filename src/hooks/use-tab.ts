import type { ActionTabType, FormTabType } from "@/types";
import { useState } from "react";

const useTab = (initialTab: ActionTabType | FormTabType) => {
    const [currTab, setCurrTab] = useState<ActionTabType | FormTabType>(initialTab);

    const handleTabChange = (tab: ActionTabType | FormTabType) => {
        if (currTab !== tab) {
            setCurrTab(tab);
        }
    };

    return { currTab, setCurrTab, handleTabChange };
};

export { useTab };
