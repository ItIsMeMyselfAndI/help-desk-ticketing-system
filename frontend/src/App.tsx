import { AppSidebar } from "./components/AppSidebar.tsx";
import { SidebarProvider, SidebarTrigger } from "./components/ui/sidebar.tsx";
import { TicketProvider } from "./contexts/TicketContext.tsx";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage.tsx";
import TicketsPage from "./pages/ViewTickets.tsx";
import NewTicketPage from "./pages/NewTicketPage.tsx";
import InboxPage from "./pages/InboxPage.tsx";
import { APP_MIN_HEIGHT, MAIN_MIN_WIDTH } from "./data/constants.ts";

const App = () => {
    return (
        <BrowserRouter>
            <SidebarProvider>
                <AppSidebar />
                <SidebarTrigger className="scale-150 sticky top-4 lg:hidden" />

                <div
                    className={`flex flex-col h-[100vh] w-[100vw]`}
                    style={{ minHeight: APP_MIN_HEIGHT, minWidth: MAIN_MIN_WIDTH }}
                >
                    <TicketProvider>
                        <Routes>
                            <Route path="/" element={<DashboardPage />} />
                            <Route path="/view-tickets" element={<TicketsPage />} />
                            <Route path="/new-ticket" element={<NewTicketPage />} />
                            <Route path="/inbox" element={<InboxPage />} />
                        </Routes>
                    </TicketProvider>
                </div>
            </SidebarProvider>
        </BrowserRouter>
    );
};

export default App;
