"use client";
import { useState } from "react";
import { ChevronDownIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

type DatePickerProps = {
  placeholder: string;
};

export function DatePicker({ placeholder }: DatePickerProps) {
  const [open, setOpen] = useState(false);
  const [date, setDate] = useState<Date | undefined>(undefined);

  return (
    <div className="flex h-full flex-col gap-3">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            id="date"
            className={`h-full w-full justify-between text-xl font-normal bg-muted border-input ${
              typeof date !== "object" && "text-foreground/50"
            }`}
          >
            {date ? date.toLocaleDateString() : `Select ${placeholder}`}
            <ChevronDownIcon />
          </Button>
        </PopoverTrigger>

        <PopoverContent className="w-auto overflow-hidden p-0" align="start">
          <Calendar
            mode="single"
            selected={date}
            captionLayout="dropdown"
            onSelect={(date) => {
              setDate(date);
              setOpen(false);
            }}
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}
