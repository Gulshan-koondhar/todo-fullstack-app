'use client';

import { KanbanTaskCard } from './KanbanTaskCard';
import { EmptyState } from './EmptyState';
import type { Task } from '@/lib/validations';

interface KanbanColumnProps {
  title: string;
  status: 'backlog' | 'doing' | 'completed';
  tasks: Task[];
  onTaskUpdate: (taskId: string, updates: Partial<Task>) => void;
  onTaskCreate: (taskData: { title: string; description?: string }) => void;
  onTaskDelete: (taskId: string) => void;
  onAddTask: (column: 'backlog' | 'doing' | 'completed') => void;
}

export function KanbanColumn({ title, status, tasks, onTaskUpdate, onTaskCreate, onTaskDelete, onAddTask }: KanbanColumnProps) {
  // Use the tasks passed from the parent, no additional filtering needed
  // The parent (KanbanBoard) should handle distributing tasks to appropriate columns

  return (
    <div className="bg-muted/50 rounded-lg p-4 min-h-[500px]">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-lg capitalize">{title}</h3>
        <span className="bg-primary text-primary-foreground text-xs font-medium px-2 py-1 rounded-full">
          {tasks.length}
        </span>
      </div>

      <div className="space-y-3 min-h-[400px]">
        {tasks.length > 0 ? (
          tasks.map(task => (
            <KanbanTaskCard
              key={task.id}
              task={task}
              onToggle={() => onTaskUpdate(task.id, { completed: !task.completed })}
              onMoveToDoing={status === 'backlog' ? () => onTaskUpdate(task.id, { inProgress: true }) : undefined}
              onMoveToBacklog={status === 'doing' ? () => onTaskUpdate(task.id, { inProgress: false }) : undefined}
              onEdit={() => {
                // For now, we'll just pass the task to the parent for editing
                console.log('Edit task:', task);
              }}
              onDelete={() => onTaskDelete(task.id)}
            />
          ))
        ) : (
          <EmptyState columnId={status} onAddTask={() => onAddTask(status)} />
        )}
      </div>
    </div>
  );
}