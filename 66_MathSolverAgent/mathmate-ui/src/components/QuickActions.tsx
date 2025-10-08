import { Button } from "./ui/button";
import { Calculator, TrendingUp, PieChart, Binary } from "lucide-react";

interface QuickActionsProps {
  onSelect: (prompt: string) => void;
}

const quickPrompts = [
  { icon: Calculator, label: "Solve equation", prompt: "Solve this equation: 2x + 5 = 15" },
  { icon: TrendingUp, label: "Calculate slope", prompt: "Find the slope of line through (2,3) and (5,9)" },
  { icon: PieChart, label: "Find area", prompt: "Calculate the area of a circle with radius 7" },
  { icon: Binary, label: "Convert base", prompt: "Convert 42 from decimal to binary" },
];

export const QuickActions = ({ onSelect }: QuickActionsProps) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {quickPrompts.map((item, index) => (
        <Button
          key={index}
          variant="outline"
          onClick={() => onSelect(item.prompt)}
          className="h-auto flex-col gap-2 p-4 border-2 hover:border-primary hover:bg-primary/5 transition-all duration-200"
        >
          <item.icon className="w-5 h-5 text-primary" />
          <span className="text-xs font-medium">{item.label}</span>
        </Button>
      ))}
    </div>
  );
};
