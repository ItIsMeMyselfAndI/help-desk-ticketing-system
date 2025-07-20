import { TicketTable } from "@/components/TicketTable";

const TicketsPage = () => {
    return (
        <div className="h-[100vh] p-4">
            <TicketTable variant="combo" />
        </div>
    );
};

export default TicketsPage;
