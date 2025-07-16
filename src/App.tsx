import { AppSidebar } from "./components/AppSidebar.tsx";
import HomePage from "./pages/HomePage.tsx";
import { SidebarProvider, SidebarTrigger } from "./components/ui/sidebar.tsx";
import { TicketProvider } from "./contexts/TicketContext.tsx";

const App = () => {
    return (
        <SidebarProvider>
            <AppSidebar></AppSidebar>

            <SidebarTrigger className="scale-150 mt-4 sticky top-4 rounded-r-xl ml-1 lg:hidden" />

            <div className="flex flex-col w-full h-[100vh]">
                <TicketProvider>
                    <HomePage />
                </TicketProvider>
            </div>
        </SidebarProvider>
    );
};

export default App;
