"use client";

import { useState } from "react";
import { TaskList } from "@/components/task/task-list";
import { TaskForm } from "@/components/task/task-form";
import { AddTaskButton } from "@/components/task/add-task-button";
import { useTasks } from "@/hooks/use-tasks";
import type { Task, CreateTaskRequest, UpdateTaskRequest } from "@/lib/validations";
import { auth } from "@/lib/auth";

export default function TasksPage() {
  const {
    tasks,
    isLoading,
    createTask,
    updateTask,
    deleteTask,
    toggleTask,
  } = useTasks();

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleAddTask = () => {
    setEditingTask(null);
    setIsFormOpen(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsFormOpen(true);
  };

  const handleFormSubmit = async (data: CreateTaskRequest | UpdateTaskRequest) => {
    setIsSubmitting(true);
    try {
      if (editingTask) {
        await updateTask(editingTask.id, data as UpdateTaskRequest);
      } else {
        await createTask(data as CreateTaskRequest);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <TaskList
        tasks={tasks}
        onToggle={toggleTask}
        onEdit={handleEditTask}
        onDelete={deleteTask}
        isLoading={isLoading}
      />

      <AddTaskButton onClick={handleAddTask} isLoading={isSubmitting} />

      <TaskForm
        open={isFormOpen}
        onOpenChange={setIsFormOpen}
        onSubmit={handleFormSubmit}
        task={editingTask}
        isLoading={isSubmitting}
      />
    </div>
  );
}
