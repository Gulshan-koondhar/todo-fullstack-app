'use client';

import type { Task } from '@/lib/validations';

interface InsightsPanelProps {
  tasks: Task[];
}

export function InsightsPanel({ tasks }: InsightsPanelProps) {
  const completedTasks = tasks.filter(task => task.completed);
  const totalTasks = tasks.length;
  const completionPercentage = totalTasks > 0 ? Math.round((completedTasks.length / totalTasks) * 100) : 0;

  // For simplicity, we'll calculate weekly stats based on current date
  const now = new Date();
  const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

  const tasksCompletedThisWeek = tasks.filter(task =>
    task.completed && new Date(task.updatedAt) > oneWeekAgo
  ).length;

  const tasksCreatedThisWeek = tasks.filter(task =>
    new Date(task.createdAt) > oneWeekAgo
  ).length;

  return (
    <div className="bg-card border rounded-lg p-4 h-fit sticky top-4">
      <h3 className="font-semibold text-lg mb-4">Insights</h3>

      <div className="space-y-4">
        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Progress</span>
            <span>{completionPercentage}%</span>
          </div>
          <div className="w-full bg-muted rounded-full h-2.5">
            <div
              className="bg-green-500 h-2.5 rounded-full transition-all duration-500 ease-in-out"
              style={{ width: `${completionPercentage}%` }}
            ></div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-500">{completedTasks.length}</div>
            <div className="text-xs text-muted-foreground">Completed</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{totalTasks}</div>
            <div className="text-xs text-muted-foreground">Total</div>
          </div>
        </div>

        {/* Weekly Stats */}
        <div className="pt-2 border-t">
          <h4 className="text-sm font-medium mb-2">This Week</h4>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Tasks Completed</span>
              <span className="font-medium">{tasksCompletedThisWeek}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Tasks Created</span>
              <span className="font-medium">{tasksCreatedThisWeek}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}