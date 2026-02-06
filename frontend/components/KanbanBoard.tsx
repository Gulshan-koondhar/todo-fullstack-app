'use client';

import { KanbanColumn } from './KanbanColumn';
import { KanbanTaskCard } from './KanbanTaskCard';
import { InsightsPanel } from './InsightsPanel';
import { ProjectHeader } from './ProjectHeader';
import { useTasks } from '@/hooks/use-tasks';
import type { Task } from '@/lib/validations';

interface KanbanBoardProps {
  tasks: Task[];
  onTaskUpdate: (taskId: string, updates: Partial<Task>) => void;
  onTaskCreate: (taskData: { title: string; description?: string }) => void;
  onTaskDelete: (taskId: string) => void;
  onAddTask: (column: 'backlog' | 'doing' | 'completed') => void;
  isLoading?: boolean;
}

export function KanbanBoard({ tasks, onTaskUpdate, onTaskCreate, onTaskDelete, onAddTask, isLoading }: KanbanBoardProps) {
  // Distribute tasks based on their status
  const backlogTasks = tasks.filter(task => !task.completed && !task.inProgress);
  const doingTasks = tasks.filter(task => !task.completed && task.inProgress);
  const completedTasks = tasks.filter(task => task.completed);

  return (
    <div className="flex flex-col h-full">
      <div className="flex flex-1 overflow-hidden">
        {/* Main Kanban Board Area */}
        <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-4 p-4 overflow-x-auto">
          <KanbanColumn
            title="Backlog"
            status="backlog"
            tasks={backlogTasks}
            onTaskUpdate={onTaskUpdate}
            onTaskCreate={onTaskCreate}
            onTaskDelete={onTaskDelete}
            onAddTask={onAddTask}
          />

          <KanbanColumn
            title="Doing"
            status="doing"
            tasks={doingTasks}
            onTaskUpdate={onTaskUpdate}
            onTaskCreate={onTaskCreate}
            onTaskDelete={onTaskDelete}
            onAddTask={onAddTask}
          />

          <KanbanColumn
            title="Completed"
            status="completed"
            tasks={completedTasks}
            onTaskUpdate={onTaskUpdate}
            onTaskCreate={onTaskCreate}
            onTaskDelete={onTaskDelete}
            onAddTask={onAddTask}
          />
        </div>

        {/* Insights Panel */}
        <div className="w-64 p-4 hidden lg:block">
          <InsightsPanel tasks={tasks} />
        </div>
      </div>
    </div>
  );
}