"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Pencil, Trash2 } from "lucide-react";
import type { Task } from "@/lib/validations";
import { cn } from "@/lib/utils";

interface KanbanTaskCardProps {
  task: Task;
  onToggle: () => void;
  onMoveToDoing?: () => void;
  onMoveToBacklog?: () => void;
  onEdit: () => void;
  onDelete: () => void;
}

export function KanbanTaskCard({
  task,
  onToggle,
  onMoveToDoing,
  onMoveToBacklog,
  onEdit,
  onDelete,
}: KanbanTaskCardProps) {
  return (
    <Card
      className={cn(
        "transition-all duration-300 shadow-md hover:shadow-lg hover:scale-[1.02] transition-transform duration-200 ease-in-out focus:ring-2 focus:ring-blue-500",
        task.completed &&
          "line-through text-gray-400 bg-green-50 dark:bg-green-900/20",
      )}
    >
      <CardContent className="pt-4">
        <div className="flex items-start gap-3">
          <Checkbox
            id={`task-${task.id}`}
            checked={task.completed}
            onCheckedChange={onToggle}
            className="mt-1"
          />
          <div className="flex-1 min-w-0">
            <label
              htmlFor={`task-${task.id}`}
              className={cn(
                "block text-base font-medium leading-tight cursor-pointer",
                task.completed && "line-through text-gray-400",
              )}
            >
              {task.title}
            </label>
            {task.description && (
              <p
                className={cn(
                  "mt-1 text-sm text-muted-foreground",
                  task.completed && "text-gray-400",
                )}
              >
                {task.description}
              </p>
            )}
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex justify-end pt-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={onEdit}
          className="text-muted-foreground hover:text-foreground"
        >
          <Pencil className="h-4 w-4 mr-1" />
        </Button>
        {/* Add move buttons based on current column */}
        {onMoveToDoing && (
          <Button
            variant="outline"
            size="sm"
            onClick={onMoveToDoing}
            className="text-muted-foreground hover:text-primary"
          >
            Move to Doing
          </Button>
        )}
        {onMoveToBacklog && (
          <Button
            variant="outline"
            size="sm"
            onClick={onMoveToBacklog}
            className="text-muted-foreground hover:text-primary"
          >
            Move to Backlog
          </Button>
        )}
        <Button
          variant="ghost"
          size="sm"
          onClick={onDelete}
          className="text-muted-foreground hover:text-destructive"
        >
          <Trash2 className="h-4 w-4 mr-1" />
        </Button>
      </CardFooter>
    </Card>
  );
}
