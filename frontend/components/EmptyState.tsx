'use client';

import { Button } from '@/components/ui/button';
import { Clipboard } from 'lucide-react';

interface EmptyStateProps {
  columnId: string;
  onAddTask: () => void;
}

export function EmptyState({ columnId, onAddTask }: EmptyStateProps) {
  const getColumnMessage = (columnId: string) => {
    switch (columnId) {
      case 'backlog':
        return 'No tasks in backlog yet';
      case 'doing':
        return 'No tasks in doing yet';
      case 'completed':
        return 'No tasks completed yet';
      default:
        return 'No tasks yet';
    }
  };

  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
        <Clipboard className="w-8 h-8 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-medium text-foreground mb-1">{getColumnMessage(columnId)}</h3>
      <p className="text-sm text-muted-foreground mb-4">
        Get started by adding a new task
      </p>
      <Button
        onClick={onAddTask}
        className="bg-primary hover:bg-primary/90 text-primary-foreground"
      >
        + Add Task
      </Button>
    </div>
  );
}