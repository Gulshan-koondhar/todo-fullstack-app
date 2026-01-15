/**
 * Service for handling todo display operations and formatting
 */

class TodoDisplayService {
  /**
   * Format a single todo for display
   */
  static formatTodo(todo) {
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
  static formatTodos(todos) {
    if (!Array.isArray(todos)) return [];

    return todos.map(todo => this.formatTodo(todo));
  }

  /**
   * Filter todos by completion status
   */
  static filterTodosByStatus(todos, status) {
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
  static sortTodos(todos, sortBy = 'createdAt', order = 'asc') {
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
   * Search todos by title or description
   */
  static searchTodos(todos, searchTerm) {
    if (!Array.isArray(todos) || !searchTerm) return todos;

    const term = searchTerm.toLowerCase();

    return todos.filter(todo =>
      (todo.title && todo.title.toLowerCase().includes(term)) ||
      (todo.description && todo.description.toLowerCase().includes(term))
    );
  }

  /**
   * Get statistics about todos
   */
  static getTodoStats(todos) {
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
   * Group todos by date range
   */
  static groupTodosByDate(todos, range = 'week') {
    if (!Array.isArray(todos)) return {};

    const groups = {};

    todos.forEach(todo => {
      let dateKey;

      switch (range) {
        case 'day':
          dateKey = new Date(todo.created_at).toDateString();
          break;
        case 'week':
          // Get the Monday of the week
          const date = new Date(todo.created_at);
          const day = date.getDay();
          const diff = date.getDate() - day + (day === 0 ? -6 : 1); // Adjust when Sunday is the first day
          const monday = new Date(date.setDate(diff));
          dateKey = monday.toDateString();
          break;
        case 'month':
          dateKey = new Date(todo.created_at).toISOString().slice(0, 7); // YYYY-MM
          break;
        case 'year':
          dateKey = new Date(todo.created_at).getFullYear().toString();
          break;
        default:
          dateKey = 'all';
      }

      if (!groups[dateKey]) {
        groups[dateKey] = [];
      }
      groups[dateKey].push(todo);
    });

    return groups;
  }

  /**
   * Format todos for export
   */
  static exportTodos(todos, format = 'json') {
    if (!Array.isArray(todos)) return '';

    const formattedTodos = this.formatTodos(todos);

    switch (format) {
      case 'json':
        return JSON.stringify(formattedTodos, null, 2);
      case 'csv':
        if (formattedTodos.length === 0) return '';

        const headers = Object.keys(formattedTodos[0]).join(',');
        const rows = formattedTodos.map(todo =>
          Object.values(todo).map(value =>
            typeof value === 'string' ? `"${value.replace(/"/g, '""')}"` : value
          ).join(',')
        );

        return [headers, ...rows].join('\n');
      default:
        return JSON.stringify(formattedTodos, null, 2);
    }
  }
}

export default TodoDisplayService;