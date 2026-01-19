"use client";

import { TaskCard } from "./task-card";
import type { Task } from "@/lib/validations";

interface TaskListProps {
  tasks: Task[];
  onToggle: (taskId: string, completed: boolean) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => Promise<void>;
  onAddTask?: () => void;
  isLoading?: boolean;
}

export function TaskList({ tasks, onToggle, onEdit, onDelete, onAddTask, isLoading }: TaskListProps) {
  if (isLoading) {
    return (
      <div className="space-y-4" role="status" aria-label="Loading tasks">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="h-32 rounded-lg bg-muted animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
          <svg
            className="w-8 h-8 text-muted-foreground"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-foreground mb-2">No tasks yet</h3>
        <p className="text-sm text-muted-foreground mb-4">
          Create your first task to get started
        </p>
        <button
          className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors duration-200 hover:scale-[1.02] transition-transform duration-200 ease-in-out dark:hover:bg-primary/80"
          onClick={onAddTask}
        >
          Add Your First Task
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4" role="list" aria-label="Task list">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
