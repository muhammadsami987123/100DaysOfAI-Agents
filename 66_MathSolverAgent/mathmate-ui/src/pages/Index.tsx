import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { EnhancedChatInput } from "@/components/EnhancedChatInput";
import { WelcomeScreenEnhanced } from "@/components/WelcomeScreenEnhanced";
import { Sidebar } from "@/components/Sidebar";
import { Header } from "@/components/Header";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ThemeProvider } from "next-themes";
import { toast } from "sonner";

interface Message {
  id: number;
  text: string;
  isBot: boolean;
  timestamp: string;
}

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = async (text: string) => {
    const userMessage: Message = {
      id: Date.now(),
      text,
      isBot: false,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await fetch("/api/solve", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ problem: text }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const solution = await response.json();
      
      const botResponse: Message = {
        id: Date.now() + 1,
        text: solution.solution || "Sorry, I couldn't solve that problem.",
        isBot: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error("Failed to fetch solution:", error);
      toast.error("Failed to fetch solution. Please try again.");
      const errorBotResponse: Message = {
        id: Date.now() + 1,
        text: "Oops! Something went wrong while trying to solve your problem. Please try again later.",
        isBot: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages(prev => [...prev, errorBotResponse]);
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <ThemeProvider attribute="class" defaultTheme="light">
      <div className="flex h-screen bg-background">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header />

          {/* Chat Area */}
          <div className="flex-1 overflow-hidden">
            <div className="max-w-4xl mx-auto h-full flex flex-col">
              {messages.length === 0 ? (
                <WelcomeScreenEnhanced />
              ) : (
                <ScrollArea className="flex-1 px-4">
                  <div ref={scrollRef} className="py-6">
                    {messages.map((message) => (
                      <ChatMessage
                        key={message.id}
                        message={message.text}
                        isBot={message.isBot}
                        timestamp={message.timestamp}
                      />
                    ))}
                  </div>
                </ScrollArea>
              )}
            </div>
          </div>

          {/* Input Area */}
          <div className="border-t border-border bg-card/80 backdrop-blur-sm">
            <div className="max-w-4xl mx-auto px-4 py-6">
              <EnhancedChatInput 
                onSend={handleSendMessage}
                showUploadArea={messages.length === 0}
              />
            </div>
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
};

export default Index;
