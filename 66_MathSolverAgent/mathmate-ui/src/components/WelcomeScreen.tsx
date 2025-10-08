import { Brain, Sparkles } from "lucide-react";

export const WelcomeScreen = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center px-4">
      <div className="relative mb-6">
        <div className="w-20 h-20 rounded-full bg-gradient-primary flex items-center justify-center shadow-glow animate-in zoom-in duration-500">
          <Brain className="w-10 h-10 text-white" />
        </div>
        <div className="absolute -top-1 -right-1 w-6 h-6 rounded-full bg-gradient-accent flex items-center justify-center animate-in zoom-in duration-700 delay-200">
          <Sparkles className="w-3 h-3 text-white" />
        </div>
      </div>
      
      <h1 className="text-4xl font-bold mb-3 bg-gradient-primary bg-clip-text text-transparent animate-in slide-in-from-bottom-4 duration-500 delay-100">
        Math Bot
      </h1>
      
      <p className="text-lg text-muted-foreground max-w-md mb-8 animate-in slide-in-from-bottom-4 duration-500 delay-200">
        Your AI-powered mathematics assistant. Ask me anything from basic arithmetic to advanced calculus!
      </p>
      
      <div className="flex flex-wrap gap-2 justify-center max-w-2xl animate-in slide-in-from-bottom-4 duration-500 delay-300">
        {[
          "Algebra",
          "Geometry", 
          "Calculus",
          "Statistics",
          "Trigonometry",
          "Linear Algebra"
        ].map((topic) => (
          <span
            key={topic}
            className="px-3 py-1 rounded-full bg-secondary text-secondary-foreground text-sm font-medium"
          >
            {topic}
          </span>
        ))}
      </div>
    </div>
  );
};
