import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "./ui/select";

type SelectorProps = {
    id?: string;
    options: string[];
    defaultItem: string;
    selectedItem: string;
    handleSelectionChange: (value: string) => void;
    filterType?: "status" | "category" | "year" | "month" | "assignment";
};

const Selector = ({ id, options, defaultItem, selectedItem, handleSelectionChange, filterType }: SelectorProps) => {
    return (
        <Select value={selectedItem} onValueChange={handleSelectionChange}>
            <SelectTrigger
                id={id}
                className={`w-full text-foreground data-[size=default]:h-full bg-muted hover:bg-accent ${
                    selectedItem === defaultItem && "text-muted-foreground"
                }`}
            >
                <SelectValue placeholder={defaultItem} />
            </SelectTrigger>
            <SelectContent>
                <SelectGroup>
                    <SelectLabel className="text-lg text-foreground/50">{`Select ${filterType}`}</SelectLabel>
                    <SelectItem
                        className="text-muted-foreground focus:bg-accent focus:text-muted-foreground"
                        value={defaultItem}
                    >
                        {defaultItem}
                    </SelectItem>
                    {options.map((val: string) => (
                        <SelectItem key={val.toLowerCase()} className="focus:bg-primary" value={val}>
                            {val}
                        </SelectItem>
                    ))}
                </SelectGroup>
            </SelectContent>
        </Select>
    );
};

export { Selector };
