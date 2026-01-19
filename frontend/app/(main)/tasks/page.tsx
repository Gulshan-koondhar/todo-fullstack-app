'use client';

import { useState } from 'react';
import { KanbanBoard } from '@/components/KanbanBoard';
import { InsightsPanel } from '@/components/InsightsPanel';
import { ProjectHeader } from '@/components/ProjectHeader';
import { AddTaskModal } from '@/components/AddTaskModal';
import { useTasks } from '@/hooks/use-tasks';
import { useToast } from '@/hooks/use-toast';
import type { Task, CreateTaskRequest, UpdateTaskRequest } from '@/lib/validations';

export default function TasksPage() {
  const {
    tasks,
    isLoading,
    createTask,
    updateTask,
    deleteTask,
    toggleTask,
  } = useTasks();

  const { toast } = useToast();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [targetColumn, setTargetColumn] = useState<'backlog' | 'doing' | 'completed'>('backlog');

  const handleAddTask = (column: 'backlog' | 'doing' | 'completed') => {
    setTargetColumn(column);
    setIsModalOpen(true);
  };

  const handleModalSubmit = async (taskData: CreateTaskRequest) => {
    try {
      await createTask(taskData);
      setIsModalOpen(false);
      return true;
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to create task. Please try again.',
        variant: 'destructive',
      });
      return false;
    }
  };

  const handleTaskUpdate = async (taskId: string, updates: Partial<Task>) => {
    try {
      // In a more advanced system, we would have a status field
      // For now, we'll just pass the updates through
      await updateTask(taskId, updates as UpdateTaskRequest);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update task. Please try again.',
        variant: 'destructive',
      });
    }
  };

  const handleTaskDelete = async (taskId: string) => {
    try {
      await deleteTask(taskId);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete task. Please try again.',
        variant: 'destructive',
      });
    }
  };

  const handleTaskToggle = async (taskId: string, completed: boolean) => {
    try {
      await toggleTask(taskId, completed);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update task status. Please try again.',
        variant: 'destructive',
      });
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="flex">
        {/* Main Kanban Board Area */}
        <div className="flex-1 overflow-x-auto">
          <KanbanBoard
            tasks={tasks}
            onTaskUpdate={handleTaskUpdate}
            onTaskCreate={handleModalSubmit}
            onTaskDelete={handleTaskDelete}
            onAddTask={handleAddTask}
            isLoading={isLoading}
          />
        </div>
      </div>

      {/* Add Task Modal */}
      <AddTaskModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleModalSubmit}
        targetColumn={targetColumn}
      />
    </div>
  );
}