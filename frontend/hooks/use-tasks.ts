"use client";

import { useState, useEffect, useCallback } from "react";
import { useToast } from "@/hooks/use-toast";
import { api } from "@/lib/api-client";
import type { Task, CreateTaskRequest, UpdateTaskRequest, TasksListResponse } from "@/lib/validations";
import { useSession } from "@/lib/session/session-context";

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();
  const { user } = useSession();

  const fetchTasks = useCallback(async () => {
    try {
      setIsLoading(true);
      if (!user?.id) {
        setTasks([]);
        return;
      }

      const response = await api.get<TasksListResponse>(
        `/users/${user.id}/tasks`
      );
      setTasks(response.tasks);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch tasks");
      setTasks([]);
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const createTask = async (data: CreateTaskRequest) => {
    if (!user?.id) throw new Error("Not authenticated");

    const response = await api.post<Task>(
      `/users/${user.id}/tasks`,
      data
    );

    setTasks((prev) => [response, ...prev]);
    toast({
      title: "Task created",
      description: "Your task has been created successfully.",
    });

    return response;
  };

  const updateTask = async (taskId: string, data: UpdateTaskRequest) => {
    if (!user?.id) throw new Error("Not authenticated");

    const response = await api.put<Task>(
      `/users/${user.id}/tasks/${taskId}`,
      data
    );

    setTasks((prev) =>
      prev.map((task) => (task.id === taskId ? response : task))
    );

    toast({
      title: "Task updated",
      description: "Your task has been updated successfully.",
    });

    return response;
  };

  const deleteTask = async (taskId: string) => {
    if (!user?.id) throw new Error("Not authenticated");

    await api.delete(`/users/${user.id}/tasks/${taskId}`);

    setTasks((prev) => prev.filter((task) => task.id !== taskId));
    toast({
      title: "Task deleted",
      description: "Your task has been deleted successfully.",
    });
  };

  const toggleTask = async (taskId: string, completed: boolean) => {
    await updateTask(taskId, { completed });
  };

  return {
    tasks,
    isLoading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTask,
  };
}
