import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import apiService from '../../services/api';

const TodoUpdateForm = ({ todo, onUpdate, onCancel }) => {
  const [title, setTitle] = useState(todo.title || '');
  const [description, setDescription] = useState(todo.description || '');
  const [completed, setCompleted] = useState(todo.completed || false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const { getAuthToken } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.length > 255) {
      setError('Title must be 255 characters or less');
      return;
    }

    if (description && description.length > 1000) {
      setError('Description must be 1000 characters or less');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      // Get auth token
      const token = getAuthToken();
      if (!token) {
        throw new Error('User not authenticated');
      }

      // Set token in API service
      apiService.setAuthToken(token);

      // Update the todo via API
      const response = await apiService.updateTodo(todo.id, {
        title,
        description,
        completed
      });

      // Call the onUpdate callback
      if (onUpdate && typeof onUpdate === 'function') {
        onUpdate(response.todo);
      }
    } catch (err) {
      console.error('Error updating todo:', err);
      setError(err.message || 'Failed to update todo');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">Update Todo</h3>

      {error && (
        <div className="mb-3 p-2 bg-red-100 text-red-700 rounded-md text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="update-title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="update-title"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (error) setError('');
            }}
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isSubmitting}
            maxLength={255}
          />
        </div>

        <div className="mb-3">
          <label htmlFor="update-description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="update-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="2"
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isSubmitting}
            maxLength={1000}
          />
        </div>

        <div className="mb-4 flex items-center">
          <input
            type="checkbox"
            id="update-completed"
            checked={completed}
            onChange={(e) => setCompleted(e.target.checked)}
            className="h-4 w-4 text-blue-600 rounded"
            disabled={isSubmitting}
          />
          <label htmlFor="update-completed" className="ml-2 block text-sm text-gray-700">
            Mark as completed
          </label>
        </div>

        <div className="flex justify-end space-x-2">
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className={`px-4 py-2 rounded-md font-medium ${
              isSubmitting
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-gray-500 text-white hover:bg-gray-600'
            }`}
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className={`px-4 py-2 rounded-md font-medium ${
              isSubmitting
                ? 'bg-blue-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            {isSubmitting ? 'Updating...' : 'Update Todo'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TodoUpdateForm;