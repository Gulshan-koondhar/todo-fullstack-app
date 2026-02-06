import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import apiService from '../../services/api';

const TodoList = ({ filter = null, onTodoUpdate = null, compact = false }) => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { getAuthToken } = useAuth();

  // Fetch todos from API
  const fetchTodos = async () => {
    setLoading(true);
    setError('');

    try {
      const token = getAuthToken();
      if (!token) {
        throw new Error('User not authenticated');
      }

      apiService.setAuthToken(token);

      // Get todos from API, applying filter if specified
      let response;
      if (filter === 'completed') {
        response = await apiService.getTodos(true);
      } else if (filter === 'pending') {
        response = await apiService.getTodos(false);
      } else {
        response = await apiService.getTodos(); // Get all todos
      }

      setTodos(response.todos || []);
    } catch (err) {
      console.error('Error fetching todos:', err);
      setError(err.message || 'Failed to fetch todos');
    } finally {
      setLoading(false);
    }
  };

  // Refresh todos when component mounts or filter changes
  useEffect(() => {
    fetchTodos();
  }, [filter]);

  // Toggle todo completion status
  const toggleTodoCompletion = async (todoId, currentStatus) => {
    try {
      const token = getAuthToken();
      if (!token) {
        throw new Error('User not authenticated');
      }

      apiService.setAuthToken(token);

      // Toggle the completion status via API
      const response = await apiService.toggleTodoCompletion(todoId);

      // Update local state
      setTodos(prevTodos =>
        prevTodos.map(todo =>
          todo.id === todoId
            ? { ...todo, completed: response.todo.completed }
            : todo
        )
      );

      // Call callback if provided
      if (onTodoUpdate && typeof onTodoUpdate === 'function') {
        onTodoUpdate(response.todo);
      }
    } catch (err) {
      console.error('Error toggling todo completion:', err);
      setError(err.message || 'Failed to update todo');
    }
  };

  // Delete a todo
  const deleteTodo = async (todoId) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) {
      return;
    }

    try {
      const token = getAuthToken();
      if (!token) {
        throw new Error('User not authenticated');
      }

      apiService.setAuthToken(token);

      // Delete the todo via API
      await apiService.deleteTodo(todoId);

      // Update local state
      setTodos(prevTodos => prevTodos.filter(todo => todo.id !== todoId));

      // Call callback if provided
      if (onTodoUpdate && typeof onTodoUpdate === 'function') {
        onTodoUpdate(null); // Passing null indicates a deletion
      }
    } catch (err) {
      console.error('Error deleting todo:', err);
      setError(err.message || 'Failed to delete todo');
    }
  };

  // Render loading state
  if (loading) {
    return (
      <div className={`${compact ? '' : 'bg-white p-6 rounded-lg shadow-md'}`}>
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <span className="ml-3 text-gray-600">Loading todos...</span>
        </div>
      </div>
    );
  }

  // Render error state
  if (error) {
    return (
      <div className={`${compact ? '' : 'bg-white p-6 rounded-lg shadow-md'}`}>
        <div className="p-3 bg-red-100 text-red-700 rounded-md">
          Error: {error}
        </div>
      </div>
    );
  }

  // Render empty state
  if (todos.length === 0) {
    const emptyMessage = filter === 'completed'
      ? "You don't have any completed todos yet."
      : filter === 'pending'
      ? "You don't have any pending todos right now."
      : "You don't have any todos yet.";

    return (
      <div className={`${compact ? '' : 'bg-white p-6 rounded-lg shadow-md'}`}>
        <div className="text-center py-8 text-gray-500">
          <p>{emptyMessage}</p>
          {!compact && <p className="mt-2">Add a new todo to get started!</p>}
        </div>
      </div>
    );
  }

  return (
    <div className={`${compact ? '' : 'bg-white p-6 rounded-lg shadow-md'}`}>
      {!compact && (
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-800">
            {filter === 'completed' ? 'Completed Todos' :
             filter === 'pending' ? 'Pending Todos' : 'All Todos'}
            <span className="text-sm font-normal ml-2 text-gray-500">({todos.length})</span>
          </h3>
        </div>
      )}

      <div className="space-y-3">
        {todos.map((todo) => (
          <div
            key={todo.id}
            className={`flex items-center justify-between p-3 border rounded-md ${
              todo.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
            }`}
          >
            <div className="flex items-center flex-1 min-w-0">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleTodoCompletion(todo.id, todo.completed)}
                className="h-4 w-4 text-blue-600 rounded mr-3 flex-shrink-0"
              />
              <div className="min-w-0">
                <div className={`font-medium truncate ${
                  todo.completed ? 'text-gray-500 line-through' : 'text-gray-800'
                }`}>
                  {todo.title}
                </div>
                {todo.description && (
                  <div className="text-sm text-gray-500 truncate mt-1">
                    {todo.description}
                  </div>
                )}
                <div className="text-xs text-gray-400 mt-1">
                  {new Date(todo.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>

            <div className="flex space-x-2 ml-4 flex-shrink-0">
              <button
                onClick={() => deleteTodo(todo.id)}
                className="text-red-500 hover:text-red-700 p-1"
                title="Delete todo"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TodoList;