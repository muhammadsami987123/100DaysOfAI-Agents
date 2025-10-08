import { Video, FileText, MessageSquare, ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface SidebarProps {
  className?: string;
}

export const Sidebar = ({ className }: SidebarProps) => {
  const [collapsed, setCollapsed] = useState(false);

  const menuItems = [
    { icon: Video, label: "Video Gallery", path: "/videos" },
    { icon: FileText, label: "Practice Tests", path: "/tests" },
  ];

  return (
    <aside
      className={cn(
        "bg-card border-r border-border transition-all duration-300 flex flex-col",
        collapsed ? "w-16" : "w-60",
        className
      )}
    >
      {/* Toggle Button */}
      <div className="p-4 flex justify-end">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed(!collapsed)}
          className="h-8 w-8"
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 px-3 space-y-1">
        {menuItems.map((item) => (
          <Button
            key={item.label}
            variant="ghost"
            className={cn(
              "w-full justify-start gap-3 h-10",
              collapsed && "justify-center px-2"
            )}
          >
            <item.icon className="h-5 w-5 text-primary flex-shrink-0" />
            {!collapsed && <span className="text-sm">{item.label}</span>}
          </Button>
        ))}

        {!collapsed && (
          <div className="pt-6">
            <h3 className="px-3 text-xs font-semibold text-muted-foreground mb-2">
              Recent Conversations
            </h3>
            <p className="px-3 text-xs text-muted-foreground">No conversations</p>
          </div>
        )}
      </nav>

      {/* Promo Section */}
      {!collapsed && (
        <div className="p-4 m-3 rounded-lg bg-accent/10 border border-accent/20">
          <div className="text-xs font-semibold text-accent mb-1">Back to School Offer</div>
          <p className="text-xs text-foreground mb-3">
            Get 30% off MathGPT Unlimited
          </p>
          <Button size="sm" className="w-full bg-accent hover:bg-accent/90">
            Upgrade to Unlimited
          </Button>
        </div>
      )}
    </aside>
  );
};
