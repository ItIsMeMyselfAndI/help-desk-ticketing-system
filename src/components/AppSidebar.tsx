import { Home, Logs, TicketPlus, Inbox, CircleUser } from "lucide-react";

import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar";

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

// Menu items.
const items = [
    { title: "Home", url: "#", icon: Home },
    { title: "View Tickets", url: "#", icon: Logs },
    { title: "New Ticket", url: "#", icon: TicketPlus },
    { title: "Inbox", url: "#", icon: Inbox },
];

const AppSidebarContent = () => {
    return (
        <SidebarContent>
            <SidebarGroup>
                <SidebarGroupLabel className="mb-2">
                    <span>Menu</span>
                </SidebarGroupLabel>
                <SidebarGroupContent>
                    <SidebarMenu>
                        {items.map((item) => (
                            <SidebarMenuItem key={item.title}>
                                <SidebarMenuButton className="hover:bg-primary p-5 rounded-none" asChild>
                                    <a href={item.url}>
                                        <item.icon className="scale-125 mr-2" />
                                        <span>{item.title}</span>
                                    </a>
                                </SidebarMenuButton>
                            </SidebarMenuItem>
                        ))}
                    </SidebarMenu>
                </SidebarGroupContent>
            </SidebarGroup>
        </SidebarContent>
    );
};

const AppSidebarFooter = () => {
    return (
        <SidebarFooter>
            <SidebarMenu>
                <SidebarMenuItem>
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <SidebarMenuButton className="hover:bg-secondary rounded-none rounded-b-md p-6 h-20">
                                <CircleUser className="scale-200 mr-2" />
                                <span>Username</span>
                            </SidebarMenuButton>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="flex flex-col gap-1 p-1">
                            <DropdownMenuLabel>
                                <span>My Account</span>
                            </DropdownMenuLabel>
                            <DropdownMenuSeparator className="bg-gray-50 mx-0.5" />
                            <DropdownMenuItem className="p-1 rounded-none focus:bg-primary">
                                <span>Profile</span>
                            </DropdownMenuItem>
                            <DropdownMenuItem className="p-1 rounded-none rounded-b-md focus:bg-primary">
                                <span>Sign Out</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </SidebarMenuItem>
            </SidebarMenu>
        </SidebarFooter>
    );
};

export function AppSidebar() {
    return (
        <Sidebar variant="floating">
            <AppSidebarContent />
            <AppSidebarFooter />
        </Sidebar>
    );
}
