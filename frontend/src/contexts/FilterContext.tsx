import React, { createContext, useContext, useState, type ReactNode } from "react";

type FilterContextType = {
    isReset: boolean;
    selectedFilterByStatus: string;
    selectedFilterByYear: string;
    selectedFilterByMonth: string;
    selectedFilterByAssignment: string;
    setIsReset: React.Dispatch<React.SetStateAction<boolean>>;
    setSelectedFilterByStatus: React.Dispatch<React.SetStateAction<string>>;
    setSelectedFilterByYear: React.Dispatch<React.SetStateAction<string>>;
    setSelectedFilterByMonth: React.Dispatch<React.SetStateAction<string>>;
    setSelectedFilterByAssignment: React.Dispatch<React.SetStateAction<string>>;
};

const FilterContext = createContext<FilterContextType | undefined>(undefined);

const FilterProvider = ({ children }: { children: ReactNode }) => {
    const [isReset, setIsReset] = useState<boolean>(false);
    const [selectedFilterByStatus, setSelectedFilterByStatus] = useState<string>("None");
    const [selectedFilterByYear, setSelectedFilterByYear] = useState<string>("None");
    const [selectedFilterByMonth, setSelectedFilterByMonth] = useState<string>("None");
    const [selectedFilterByAssignment, setSelectedFilterByAssignment] = useState<string>("None");

    return (
        <FilterContext.Provider
            value={{
                // states
                isReset,
                selectedFilterByStatus,
                selectedFilterByAssignment,
                selectedFilterByYear,
                selectedFilterByMonth,
                // setters
                setIsReset,
                setSelectedFilterByStatus,
                setSelectedFilterByYear,
                setSelectedFilterByMonth,
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
