import { Logs, TicketPlus, Inbox, CircleUser, LayoutDashboard } from "lucide-react";

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
import { Link, useLocation } from "react-router-dom";

// Menu items.
const items = [
    { title: "Dashboard", route: "/", icon: LayoutDashboard },
    { title: "View Tickets", route: "/view-tickets", icon: Logs },
    { title: "New Ticket", route: "/new-ticket", icon: TicketPlus },
    { title: "Inbox", route: "/inbox", icon: Inbox },
];

const AppSidebarContent = () => {
    const location = useLocation();

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
                                <SidebarMenuButton
                                    className={`hover:bg-primary p-5 rounded-none ${
                                        location.pathname === item.route &&
                                        "text-primary hover:text-foreground font-bold"
                                    }`}
                                    asChild
                                >
                                    <Link to={item.route}>
                                        <item.icon className="scale-125 mr-2" />
                                        <span>{item.title}</span>
                                    </Link>
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
