import { AppSidebar } from "./components/AppSidebar.tsx";
import HomePage from "./pages/HomePage.tsx";
import { SidebarProvider, SidebarTrigger } from "./components/ui/sidebar.tsx";

const App = () => {
  return (
    <SidebarProvider className="h-screen">
      <AppSidebar></AppSidebar>

      <SidebarTrigger className="scale-150 mt-4 sticky top-4 rounded-r-xl ml-1" />

      <div className="flex flex-col w-full h-full p-6">
        <HomePage />
      </div>
    </SidebarProvider>
  );
};

export default App;
