import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import apiService from '../../services/api';

const TodoCreationForm = ({ onTodoCreated = null, compact = false }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
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

      // Create the todo via API
      const response = await apiService.createTodo(title, description);

      // Reset form
      setTitle('');
      setDescription('');
      setError('');

      // Call callback if provided
      if (onTodoCreated && typeof onTodoCreated === 'function') {
        onTodoCreated(response.todo);
      }
    } catch (err) {
      console.error('Error creating todo:', err);
      setError(err.message || 'Failed to create todo');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (compact) {
    return (
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (error) setError('');
          }}
          placeholder="Add a new todo..."
          className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          disabled={isSubmitting}
          maxLength={255}
        />
        <button
          type="submit"
          disabled={isSubmitting || !title.trim()}
          className={`px-4 py-2 rounded font-medium text-sm ${
            isSubmitting || !title.trim()
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-green-500 text-white hover:bg-green-600'
          }`}
        >
          {isSubmitting ? 'Adding...' : 'Add'}
        </button>
      </form>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Create New Todo</h3>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (error) setError('');
            }}
            placeholder="What needs to be done?"
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isSubmitting}
            maxLength={255}
          />
          <p className="mt-1 text-xs text-gray-500">Required, 1-255 characters</p>
        </div>

        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Additional details (optional)"
            rows="3"
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isSubmitting}
            maxLength={1000}
          />
          <p className="mt-1 text-xs text-gray-500">Optional, max 1000 characters</p>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting || !title.trim()}
            className={`px-6 py-2 rounded-md font-medium ${
              isSubmitting || !title.trim()
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            {isSubmitting ? 'Creating...' : 'Create Todo'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TodoCreationForm;