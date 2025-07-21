import { AppSidebar } from "./components/AppSidebar.tsx";
import { SidebarProvider, SidebarTrigger } from "./components/ui/sidebar.tsx";
import { TicketProvider } from "./contexts/TicketContext.tsx";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage.tsx";
import TicketsPage from "./pages/TicketsPage.tsx";
import NewTicketPage from "./pages/NewTicketPage.tsx";
import InboxPage from "./pages/InboxPage.tsx";

const App = () => {
    return (
        <BrowserRouter>
            <SidebarProvider>
                <AppSidebar />
                <SidebarTrigger className="scale-150 mt-4 sticky top-4 rounded-r-xl ml-1 lg:hidden" />

                <div className="flex flex-col w-full h-[100vh] p-4">
                    <TicketProvider>
                        <Routes>
                            <Route path="/" element={<HomePage />} />
                            <Route path="/tickets" element={<TicketsPage />} />
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
