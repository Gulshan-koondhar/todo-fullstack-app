/**
 * Todo Actions Handler
 * Contains utility functions for handling todo actions in the UI
 */

class TodoActions {
  constructor(apiService) {
    this.apiService = apiService;
  }

  /**
   * Toggle the completion status of a todo
   */
  async toggleCompletion(todoId, currentStatus, authToken) {
    try {
      // Set auth token in API service
      this.apiService.setAuthToken(authToken);

      // Call the API to toggle completion
      const response = await this.apiService.toggleTodoCompletion(todoId);

      if (response.success) {
        return {
          success: true,
          todo: response.todo,
          message: response.todo.completed ? 'Todo marked as completed' : 'Todo marked as pending'
        };
      } else {
        return {
          success: false,
          error: response.error || 'Failed to toggle completion status'
        };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message || 'Error toggling completion status'
      };
    }
  }

  /**
   * Update a todo item
   */
  async updateTodo(todoId, updates, authToken) {
    try {
      // Set auth token in API service
      this.apiService.setAuthToken(authToken);

      // Call the API to update the todo
      const response = await this.apiService.updateTodo(todoId, updates);

      if (response.success) {
        return {
          success: true,
          todo: response.todo,
          message: 'Todo updated successfully'
        };
      } else {
        return {
          success: false,
          error: response.error || 'Failed to update todo'
        };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message || 'Error updating todo'
      };
    }
  }

  /**
   * Delete a todo item
   */
  async deleteTodo(todoId, authToken) {
    try {
      // Set auth token in API service
      this.apiService.setAuthToken(authToken);

      // Call the API to delete the todo
      const response = await this.apiService.deleteTodo(todoId);

      if (response.success) {
        return {
          success: true,
          message: response.message || 'Todo deleted successfully'
        };
      } else {
        return {
          success: false,
          error: response.error || 'Failed to delete todo'
        };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message || 'Error deleting todo'
      };
    }
  }

  /**
   * Format a todo for display
   */
  formatTodoForDisplay(todo) {
    if (!todo) return null;

    return {
      id: todo.id,
      title: todo.title || 'Untitled',
      description: todo.description || '',
      completed: Boolean(todo.completed),
      createdAt: new Date(todo.created_at).toLocaleDateString(),
      updatedAt: new Date(todo.updated_at).toLocaleDateString(),
      displayTitle: todo.title || 'Untitled',
      displayDescription: todo.description || 'No description',
      status: todo.completed ? 'completed' : 'pending',
      statusIcon: todo.completed ? '✓' : '○'
    };
  }

  /**
   * Format multiple todos for display
   */
  formatTodosForDisplay(todos) {
    if (!Array.isArray(todos)) return [];

    return todos.map(todo => this.formatTodoForDisplay(todo));
  }

  /**
   * Filter todos by completion status
   */
  filterTodosByStatus(todos, status) {
    if (!Array.isArray(todos)) return [];

    switch (status) {
      case 'completed':
        return todos.filter(todo => todo.completed);
      case 'pending':
        return todos.filter(todo => !todo.completed);
      case 'all':
      default:
        return todos;
    }
  }

  /**
   * Sort todos by various criteria
   */
  sortTodos(todos, sortBy = 'createdAt', order = 'asc') {
    if (!Array.isArray(todos)) return [];

    return [...todos].sort((a, b) => {
      let comparison = 0;

      switch (sortBy) {
        case 'title':
          comparison = a.title.localeCompare(b.title);
          break;
        case 'createdAt':
          comparison = new Date(a.created_at) - new Date(b.created_at);
          break;
        case 'updatedAt':
          comparison = new Date(a.updated_at) - new Date(b.updated_at);
          break;
        case 'completed':
          comparison = a.completed === b.completed ? 0 : a.completed ? 1 : -1;
          break;
        default:
          comparison = new Date(a.created_at) - new Date(b.created_at);
      }

      return order === 'desc' ? -comparison : comparison;
    });
  }

  /**
   * Get statistics about todos
   */
  getTodoStats(todos) {
    if (!Array.isArray(todos)) {
      return {
        total: 0,
        completed: 0,
        pending: 0,
        completionRate: 0
      };
    }

    const total = todos.length;
    const completed = todos.filter(todo => todo.completed).length;
    const pending = total - completed;
    const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

    return {
      total,
      completed,
      pending,
      completionRate
    };
  }

  /**
   * Validate todo data before submission
   */
  validateTodoData(data) {
    const errors = [];

    if (!data.title || typeof data.title !== 'string' || data.title.trim().length === 0) {
      errors.push('Title is required');
    } else if (data.title.length > 255) {
      errors.push('Title must be 255 characters or less');
    }

    if (data.description && typeof data.description === 'string' && data.description.length > 1000) {
      errors.push('Description must be 1000 characters or less');
    }

    if ('completed' in data && typeof data.completed !== 'boolean') {
      errors.push('Completion status must be a boolean value');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}

export default TodoActions;