"use client";

import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

interface AddTaskButtonProps {
  onClick: () => void;
  isLoading?: boolean;
}

export function AddTaskButton({ onClick, isLoading }: AddTaskButtonProps) {
  return (
    <>
      {/* Desktop: Fixed button */}
      <Button
        onClick={onClick}
        disabled={isLoading}
        className="hidden md:flex fixed bottom-24 right-8 h-14 w-14 rounded-full shadow-lg"
        size="icon"
        aria-label="Add new task"
      >
        <Plus className="h-6 w-6" />
      </Button>

      {/* Mobile: Floating Action Button */}
      <Button
        onClick={onClick}
        disabled={isLoading}
        className="md:hidden fixed bottom-24 right-6 h-14 w-14 rounded-full shadow-lg"
        size="icon"
        aria-label="Add new task"
      >
        <Plus className="h-6 w-6" />
      </Button>
    </>
  );
}
