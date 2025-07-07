import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectLabel,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DatePicker } from "@/components/ui/date-picker";
import { Checkbox } from "@/components/ui/checkbox";
import { useState } from "react";

type SummaryCardProps = {
  status: string;
  count: number;
};

const SummaryCard = ({ status, count }: SummaryCardProps) => {
  return (
    <Card className="grow gap-0 h-50">
      <CardHeader className="text-foreground/80 text-xl leading-none text-left">
        {status}
      </CardHeader>
      <CardContent className="flex text-primary justify-center text-5xl leading-none m-auto">
        {count}
      </CardContent>
    </Card>
  );
};

const SummarySection = () => {
  return (
    <div className="flex gap-4">
      <SummaryCard status="Unassigned" count={100}></SummaryCard>
      <SummaryCard status="In Progress" count={100}></SummaryCard>
      <SummaryCard status="Resolved" count={100}></SummaryCard>
      <SummaryCard status="Closed" count={100}></SummaryCard>
    </div>
  );
};

type Ticket = {
  id: string;
  title: string;
  status: "Unassigned" | "In Progress" | "Resolved" | "Closed";
  created_at: string;
  updated_at: string;
  assigned_to: string;
};

const tickets: Ticket[] = [
  {
    id: "T-1",
    title: "my 1st ticket mf",
    status: "Unassigned",
    created_at: "2024-10-09",
    updated_at: "2024-10-09",
    assigned_to: "@bentot",
  },
  {
    id: "T-2",
    title: "my 2nd ticket mf",
    status: "In Progress",
    created_at: "2024-10-09",
    updated_at: "2024-10-09",
    assigned_to: "@juantot",
  },
  {
    id: "T-3",
    title: "my 3rd ticket mf",
    status: "Resolved",
    created_at: "2024-10-09",
    updated_at: "2024-10-09",
    assigned_to: "@gwentot",
  },
  {
    id: "T-4",
    title: "my 4th ticket mf",
    status: "Closed",
    created_at: "2024-10-09",
    updated_at: "2024-10-09",
    assigned_to: "@kwintot",
  },
];

const cloneArray = <T,>(arr: T[], count: number) => {
  return modToUniqueTicketIDs(Array(count).fill(arr).flat());
};

const modToUniqueTicketIDs = (tickets: Ticket[]) => {
  tickets.forEach((ticket, index) => (ticket.id = `T-${index}`));
  return tickets;
};

type TicketTableProps = {
  tickets: Ticket[];
};

const TicketTable = ({ tickets }: TicketTableProps) => {
  const [selectedRows, setSelectedRows] = useState<Set<string>>(new Set());

  const toggleRowSelection = (id: string) => {
    setSelectedRows((prev) => {
      const selectedRowsCopy = new Set(prev); // Create a copy
      if (selectedRowsCopy.has(id)) {
        selectedRowsCopy.delete(id);
      } else {
        selectedRowsCopy.add(id);
      }
      return selectedRowsCopy; // Return the new Set
    });
  };

  const chooseStatusColor = (status: Ticket["status"]) => {
    switch (status) {
      case "Unassigned":
        return "bg-gray-500";
      case "In Progress":
        return "bg-blue-500";
      case "Resolved":
        return "bg-green-500";
      case "Closed":
        return "bg-yellow-500";
      default:
        return "";
    }
  };

  return (
    <Table className="bg-card">
      <TableHeader className="text-xl bg-muted h-15">
        <TableRow key="header">
          <TableHead className="text-primary pl-5">Edit</TableHead>
          <TableHead className="text-primary">Ticket</TableHead>
          <TableHead className="text-primary">Title</TableHead>
          <TableHead className="text-primary">Status</TableHead>
          <TableHead className="text-primary text-right pr-5">
            Assigned To
          </TableHead>
        </TableRow>
      </TableHeader>

      <TableBody className="text-lg">
        {cloneArray(tickets, 20).map((ticket) => (
          <TableRow
            key={ticket.id}
            onClick={() => toggleRowSelection(ticket.id)}
          >
            <TableCell className="pl-5">
              <Checkbox
                checked={selectedRows.has(ticket.id)}
                className="size-5 bg-muted"
              />
            </TableCell>
            <TableCell>{ticket.id}</TableCell>
            <TableCell>{ticket.title}</TableCell>
            <TableCell>
              <span
                className={`${chooseStatusColor(
                  ticket.status
                )} p-1 rounded-xl text-center`}
              >
                {ticket.status}
              </span>
            </TableCell>
            <TableCell className="text-right pr-5">
              {ticket.assigned_to}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

type FilterSelectionProps = {
  placeholder: string;
  values: string[];
};

const FilterSelection = ({ placeholder, values }: FilterSelectionProps) => {
  return (
    <Select>
      <SelectTrigger className="w-full text-sidebar-foreground data-[size=default]:h-full data-[placeholder]:text-foreground bg-muted hover:bg-accent">
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>

      <SelectContent>
        <SelectGroup>
          <SelectLabel className="text-lg">{placeholder}</SelectLabel>
          {values.map((val: string) => (
            <SelectItem className="focus:bg-primary" value={val.toLowerCase()}>
              {val}
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  );
};

const FiltersCard = () => {
  return (
    <Card className="h-full w-full px-6 gap-2">
      <CardTitle className="text-2xl text-primary">Table Filters</CardTitle>
      <CardContent className="flex flex-col justify-evenly gap-2">
        <CardDescription className="text-lg">By status</CardDescription>
        <FilterSelection
          placeholder="Status"
          values={["Unassigned", "In progress", "Resolved", "Closed"]}
        />
        <CardDescription className="text-lg">By date</CardDescription>
        <DatePicker placeholder="Date" />
        <CardDescription className="text-lg">By assignment</CardDescription>
        <FilterSelection
          placeholder="Assignment"
          values={["@johndoe", "@dora", "@patric", "@spongebob"]}
        />
      </CardContent>
    </Card>
  );
};

const HomePage = () => {
  return (
    <div className="flex flex-col gap-4 h-full w-full">
      <SummarySection />

      <div className="flex gap-4 min-h-0">
        <div className="flex-4 min-h-0 overflow-auto scroll-auto">
          <TicketTable tickets={tickets} />
        </div>

        <div className="flex-1 flex flex-col gap-4 w-full">
          <FiltersCard />

          <div className="w-full h-full bg-card border rounded-xl"></div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
