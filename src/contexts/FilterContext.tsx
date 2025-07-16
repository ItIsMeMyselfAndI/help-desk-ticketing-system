import React, { createContext, useContext, useState, type ReactNode } from "react";

type FilterContextType = {
    isReset: boolean;
    selectedFilterByStatus: string;
    selectedFilterByDate: string;
    selectedFilterByAssignment: string;
    setIsReset: React.Dispatch<React.SetStateAction<boolean>>;
    setSelectedFilterByStatus: React.Dispatch<React.SetStateAction<string>>;
    setSelectedFilterByDate: React.Dispatch<React.SetStateAction<string>>;
    setSelectedFilterByAssignment: React.Dispatch<React.SetStateAction<string>>;
};

const FilterContext = createContext<FilterContextType | undefined>(undefined);

const FilterProvider = ({ children }: { children: ReactNode }) => {
    const [isReset, setIsReset] = useState<boolean>(false);
    const [selectedFilterByStatus, setSelectedFilterByStatus] = useState<string>("None");
    const [selectedFilterByDate, setSelectedFilterByDate] = useState<string>("None");
    const [selectedFilterByAssignment, setSelectedFilterByAssignment] = useState<string>("None");

    return (
        <FilterContext.Provider
            value={{
                isReset,
                selectedFilterByStatus,
                selectedFilterByDate,
                selectedFilterByAssignment,
                setIsReset,
                setSelectedFilterByStatus,
                setSelectedFilterByDate,
                setSelectedFilterByAssignment,
            }}
        >
            {children}
        </FilterContext.Provider>
    );
};

const useFilterContext = () => {
    const context = useContext(FilterContext);
    if (!context) {
        throw new Error("useFilterContext must be used within a FilterProvider");
    }
    return context;
};

export { FilterProvider, useFilterContext };
