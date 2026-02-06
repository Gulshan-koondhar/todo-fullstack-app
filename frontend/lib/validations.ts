import { z } from "zod";

// Base task schema
export const BaseTaskSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1).max(200),
  description: z.string().max(1000).nullable(),
  completed: z.boolean(),
  inProgress: z.boolean().optional().default(false),
  user_id: z.string().uuid(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export type Task = z.infer<typeof BaseTaskSchema>;

// Create task request schema
export const CreateTaskSchema = z.object({
  title: z.string()
    .min(1, "Title is required")
    .max(200, "Title must be less than 200 characters")
    .trim()
    .refine((val) => val.trim().length > 0, "Title cannot be empty"),
  description: z.string()
    .max(1000, "Description must be less than 1000 characters")
    .optional()
    .nullable(),
});

export type CreateTaskRequest = z.infer<typeof CreateTaskSchema>;

// Update task request schema
export const UpdateTaskSchema = z.object({
  title: z.string()
    .min(1, "Title must be at least 1 character")
    .max(200, "Title must be less than 200 characters")
    .trim()
    .refine((val) => val.trim().length > 0, "Title cannot be empty")
    .optional(),
  description: z.string()
    .max(1000, "Description must be less than 1000 characters")
    .optional()
    .nullable(),
  completed: z.boolean().optional(),
  inProgress: z.boolean().optional(),
});

export type UpdateTaskRequest = z.infer<typeof UpdateTaskSchema>;

// Tasks list response schema
export const TasksListResponseSchema = z.object({
  tasks: z.array(BaseTaskSchema),
  count: z.number().int().nonnegative(),
});

export type TasksListResponse = z.infer<typeof TasksListResponseSchema>;

// Task response schema
export const TaskResponseSchema = z.object({
  task: BaseTaskSchema,
});

export type TaskResponse = z.infer<typeof TaskResponseSchema>;

// Base user schema
export const BaseUserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export type User = z.infer<typeof BaseUserSchema>;

// Create user request schema
export const CreateUserSchema = z.object({
  email: z.string().email("Invalid email format"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain at least 1 uppercase letter")
    .regex(/[a-z]/, "Password must contain at least 1 lowercase letter")
    .regex(/[0-9]/, "Password must contain at least 1 number")
    .regex(/[^A-Za-z0-9]/, "Password must contain at least 1 special character"),
  name: z.string().min(1, "Name is required"),
});

export type CreateUserRequest = z.infer<typeof CreateUserSchema>;

// User response schema
export const UserResponseSchema = z.object({
  user: BaseUserSchema,
});

export type UserResponse = z.infer<typeof UserResponseSchema>;

// Error response schema
export const ErrorResponseSchema = z.object({
  error: z.string(),
  details: z.record(z.string()).optional(),
});

export type ErrorResponse = z.infer<typeof ErrorResponseSchema>;

// List tasks query parameters
export const ListTasksParamsSchema = z.object({
  completed: z.coerce.boolean().optional(),
});

export type ListTasksParams = z.infer<typeof ListTasksParamsSchema>;
