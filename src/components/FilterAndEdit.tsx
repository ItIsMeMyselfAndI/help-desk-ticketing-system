import { FilterProvider } from "@/contexts/FilterContext";
import { TableFilter } from "./TableFIlter";
import { QuickEdit } from "./QuickEdit";
import { useEffect, useState } from "react";

const FilterAndEdit = () => {
    const [isSmallHeight, setIsSmallHeight] = useState<boolean>(false);

    useEffect(() => {
        const mediaQuery = window.matchMedia("max-h-740px");
        setIsSmallHeight(mediaQuery.matches);

        const handleHeightChange = (e: MediaQueryListEvent) => {
            setIsSmallHeight(e.matches);
        };

        mediaQuery.addEventListener("change", handleHeightChange);

        return () => mediaQuery.removeEventListener("change", handleHeightChange);
    }, []);

    return isSmallHeight ? (
        <div className="grid grid-rows-1 gap-4">
            <FilterProvider>
                <TableFilter variant="full" />
            </FilterProvider>
            <QuickEdit />
        </div>
    ) : (
        <div></div>
    );
};

export { FilterAndEdit };
