"use client";

import { useState } from "react";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Pencil, Trash2 } from "lucide-react";
import type { Task } from "@/lib/validations";
import { cn } from "@/lib/utils";

interface TaskCardProps {
  task: Task;
  onToggle: (taskId: string, completed: boolean) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => Promise<void>;
  isUpdating?: boolean;
}

export function TaskCard({ task, onToggle, onEdit, onDelete, isUpdating }: TaskCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleToggle = async () => {
    await onToggle(task.id, !task.completed);
  };

  const handleDelete = async () => {
    if (confirm("Are you sure you want to delete this task?")) {
      setIsDeleting(true);
      try {
        await onDelete(task.id);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  return (
    <Card
      className={cn(
        "transition-all duration-200",
        task.completed && "opacity-60"
      )}
    >
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-3 flex-1">
            <Checkbox
              id={`task-${task.id}`}
              checked={task.completed}
              onCheckedChange={handleToggle}
              disabled={isUpdating}
              className="mt-1"
            />
            <div className="flex-1 min-w-0">
              <label
                htmlFor={`task-${task.id}`}
                className={cn(
                  "block text-lg font-medium leading-tight cursor-pointer",
                  task.completed && "line-through text-muted-foreground"
                )}
              >
                {task.title}
              </label>
              {task.description && (
                <p
                  className={cn(
                    "mt-1 text-sm text-muted-foreground",
                    task.completed && "line-through"
                  )}
                >
                  {task.description}
                </p>
              )}
            </div>
          </div>
        </div>
      </CardHeader>
      {task.description && (
        <CardContent className="pt-0 pb-2">
          <p
            className={cn(
              "text-sm text-muted-foreground",
              task.completed && "line-through"
            )}
          >
            {task.description}
          </p>
        </CardContent>
      )}
      <CardFooter className="pt-2 flex justify-end gap-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onEdit(task)}
          disabled={isUpdating || isDeleting}
          className="text-muted-foreground hover:text-foreground"
        >
          <Pencil className="h-4 w-4 mr-1" />
          Edit
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleDelete}
          disabled={isUpdating || isDeleting}
          className="text-muted-foreground hover:text-destructive"
        >
          <Trash2 className="h-4 w-4 mr-1" />
          {isDeleting ? "Deleting..." : "Delete"}
        </Button>
      </CardFooter>
    </Card>
  );
}
