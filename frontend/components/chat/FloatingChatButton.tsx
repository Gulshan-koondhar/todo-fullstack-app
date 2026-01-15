"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { MessageCircle, X } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import ChatInterface from "@/src/components/chat/ChatInterface";

export default function FloatingChatButton() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="relative">
          <Card className="w-80 h-[500px] shadow-lg border">
            <CardContent className="p-0 h-full flex flex-col">
              <div className="flex justify-between items-center p-3 border-b">
                <h3 className="font-semibold">AI Todo Assistant</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={toggleChat}
                  aria-label="Close chat"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex-1 overflow-hidden">
                <ChatInterface />
              </div>
            </CardContent>
          </Card>
        </div>
      ) : (
        <Button
          onClick={toggleChat}
          className="rounded-full w-14 h-14 p-0 shadow-lg"
          size="lg"
          aria-label="Open chat"
        >
          <MessageCircle className="h-6 w-6" />
        </Button>
      )}
    </div>
  );
}