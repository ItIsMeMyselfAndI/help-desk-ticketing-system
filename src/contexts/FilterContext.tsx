import React, { createContext, useContext, useState, type ReactNode } from "react";

type FilterContextType = {
    isReset: boolean;
    setIsReset: React.Dispatch<React.SetStateAction<boolean>>;
    isFilteredByStatus: boolean;
    setIsFilteredByStatus: React.Dispatch<React.SetStateAction<boolean>>;
    isFilteredByDate: boolean;
    setIsFilteredByDate: React.Dispatch<React.SetStateAction<boolean>>;
    isFilteredByAssignment: boolean;
    setIsFilteredByAssignment: React.Dispatch<React.SetStateAction<boolean>>;
};

const FilterContext = createContext<FilterContextType | undefined>(undefined);

const FilterProvider = ({ children }: { children: ReactNode }) => {
    const [isReset, setIsReset] = useState<boolean>(false);
    const [isFilteredByStatus, setIsFilteredByStatus] = useState<boolean>(false);
    const [isFilteredByDate, setIsFilteredByDate] = useState<boolean>(false);
    const [isFilteredByAssignment, setIsFilteredByAssignment] = useState<boolean>(false);

    return (
        <FilterContext.Provider
            value={{
                isReset,
                setIsReset,
                isFilteredByStatus,
                setIsFilteredByStatus,
                isFilteredByDate,
                setIsFilteredByDate,
                isFilteredByAssignment,
                setIsFilteredByAssignment,
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
