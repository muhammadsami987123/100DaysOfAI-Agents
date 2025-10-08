import { useState } from "react";
import { Send, Sigma, Wrench, ArrowUp } from "lucide-react";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";
import { FileUploadArea } from "./FileUploadArea";

interface EnhancedChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  showUploadArea?: boolean;
}

export const EnhancedChatInput = ({ onSend, disabled, showUploadArea = true }: EnhancedChatInputProps) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput("");
    }
  };

  return (
    <div className="space-y-4">
      {showUploadArea && <FileUploadArea />}
      
      <form onSubmit={handleSubmit} className="relative">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question here..."
          disabled={disabled}
          rows={1}
          className={cn(
            "w-full px-4 py-4 pr-32 rounded-xl border border-border resize-none",
            "bg-background text-foreground placeholder:text-muted-foreground",
            "focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20",
            "transition-all duration-200",
            "disabled:opacity-50 disabled:cursor-not-allowed"
          )}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
        />
        
        <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
          <Button
            type="button"
            size="icon"
            variant="ghost"
            className="h-8 w-8 rounded-lg"
          >
            <Sigma className="w-4 h-4" />
          </Button>
          
          <Button
            type="button"
            size="icon"
            variant="ghost"
            className="h-8 w-8 rounded-lg"
          >
            <Wrench className="w-4 h-4" />
          </Button>
          
          <Button
            type="submit"
            size="icon"
            disabled={!input.trim() || disabled}
            className="h-9 w-9 rounded-lg bg-primary hover:bg-primary/90"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </form>

      <Button
        size="icon"
        variant="outline"
        className="fixed bottom-24 right-8 h-12 w-12 rounded-full shadow-glow"
      >
        <ArrowUp className="w-5 h-5" />
      </Button>
    </div>
  );
};
