import { SquareRadical } from "lucide-react";
import { CategoryTabs } from "./CategoryTabs";
import { useState } from "react";

export const WelcomeScreenEnhanced = () => {
  const [activeCategory, setActiveCategory] = useState("MathGPT");

  return (
    <div className="flex flex-col items-center justify-center text-center px-4 py-12">
      <div className="mb-6 animate-in zoom-in duration-500">
        <div className="w-16 h-16 rounded-xl bg-primary flex items-center justify-center shadow-glow">
          <SquareRadical className="w-8 h-8 text-primary-foreground" strokeWidth={2.5} />
        </div>
      </div>
      
      <h1 className="text-4xl md:text-5xl font-bold mb-3 animate-in slide-in-from-bottom-4 duration-500 delay-100">
        MathGPT - Your Personal Math Solver
      </h1>
      
      <p className="text-base md:text-lg text-muted-foreground max-w-2xl mb-8 animate-in slide-in-from-bottom-4 duration-500 delay-200">
        Get instant homework help from your on-demand AI math solver
      </p>
      
      <div className="animate-in slide-in-from-bottom-4 duration-500 delay-300">
        <CategoryTabs 
          activeCategory={activeCategory}
          onCategoryChange={setActiveCategory}
        />
      </div>
    </div>
  );
};
