// API service for handling all API calls to the backend
import { authClient } from '@/lib/auth-client';

class ApiService {
  constructor() {
    // Ensure the base URL includes /api/v1 if not already present
    const rawBaseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    // Remove trailing slash if present
    const cleanBaseURL = rawBaseURL.endsWith('/') ? rawBaseURL.slice(0, -1) : rawBaseURL;
    // Add /api/v1 if it's not already included
    this.baseURL = cleanBaseURL.includes('/api/v1') ? cleanBaseURL : `${cleanBaseURL}/api/v1`;
    this.authToken = null;
  }

  // Helper function to decode JWT payload
  decodeJwtPayload(token) {
    try {
      // Split the JWT token (header.payload.signature)
      const parts = token.split('.');
      if (parts.length !== 3) {
        throw new Error('Invalid JWT token format');
      }

      // Decode the payload (second part)
      // JWT uses base64url encoding, which is similar to base64 but with different characters
      let payload = parts[1];
      // Replace URL-safe base64 characters with standard base64
      payload = payload.replace(/-/g, '+').replace(/_/g, '/');

      // Pad the string if needed
      while (payload.length % 4) {
        payload += '=';
      }

      // Decode from base64
      const decodedPayload = atob(payload);
      return JSON.parse(decodedPayload);
    } catch (error) {
      console.error('Error decoding JWT token:', error);
      throw new Error('Could not decode authentication token');
    }
  }

  // Get authentication token from Better Auth client
  async getAuthToken() {
    try {
      // First try using the Better Auth getSession method
      const session = await authClient.getSession();
      if (session?.session?.token) {
        return session.session.token;
      }

      // If that doesn't work, try the getToken helper that checks localStorage/cookies
      // Import the getToken function - we'll call it directly
      const token = this.getTokenFromStorage();
      if (token) {
        return token;
      }

      // Fallback to manually set token
      return this.authToken;
    } catch (error) {
      // Fallback to manually set token if Better Auth session is not available
      return this.authToken;
    }
  }

  // Helper function to get token from localStorage or cookies (mimics the getToken function from auth-client.ts)
  getTokenFromStorage() {
    if (typeof window === "undefined") return null;

    // First try to get from localStorage (our custom auth)
    const localToken = localStorage.getItem('auth_token');
    if (localToken) {
      return localToken;
    }

    // Fallback to Better Auth cookies
    if (typeof document !== "undefined") {
      const cookies = document.cookie.split("; ");
      const sessionCookie = cookies.find((c) =>
        c.startsWith("todo-app_session_token=")
      );

      if (sessionCookie) {
        return sessionCookie.substring("todo-app_session_token=".length);
      }
    }

    return null;
  }

  // Set authentication token manually (fallback)
  setAuthToken(token) {
    this.authToken = token;
  }

  // Remove authentication token
  removeAuthToken() {
    this.authToken = null;
  }

  // Create headers with auth token if available
  async getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    // Try to get token from Better Auth first, fallback to manually set token
    const token = await this.getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;

    // Get headers asynchronously
    const headers = await this.getHeaders();
    const config = {
      headers: {
        ...headers,
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      // If response is not ok, throw an error
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      // Handle empty response
      if (response.status === 204) {
        return null;
      }

      // Parse JSON response
      return await response.json();
    } catch (error) {
      console.error(`API request error for ${url}:`, error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // Get user info
  async getUserInfo() {
    return this.request('/users/me');
  }

  // Todo operations - These should work with the actual backend API structure
  // The backend uses /users/{user_id}/tasks, so we need to get user ID first
  async getTodos(completed = null) {
    // Extract user ID from token and call the correct endpoint
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      const params = completed !== null ? `?completed=${completed}` : '';
      return this.request(`/users/${userId}/tasks${params}`);  // baseURL already includes /api/v1
    } catch (error) {
      throw new Error(`Could not get todos: ${error.message}`);
    }
  }

  async createTodo(title, description = null) {
    // Extract user ID from token and call the correct endpoint
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      return this.request(`/users/${userId}/tasks`, {  // baseURL already includes /api/v1
        method: 'POST',
        body: JSON.stringify({ title, description }),
      });
    } catch (error) {
      throw new Error(`Could not create todo: ${error.message}`);
    }
  }

  async updateTodo(todoId, updates) {
    // Extract user ID from token and call the correct endpoint
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      return this.request(`/users/${userId}/tasks/${todoId}`, {  // baseURL already includes /api/v1
        method: 'PUT',
        body: JSON.stringify(updates),
      });
    } catch (error) {
      throw new Error(`Could not update todo: ${error.message}`);
    }
  }

  async deleteTodo(todoId) {
    // Extract user ID from token and call the correct endpoint
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      return this.request(`/users/${userId}/tasks/${todoId}`, {  // baseURL already includes /api/v1
        method: 'DELETE',
      });
    } catch (error) {
      throw new Error(`Could not delete todo: ${error.message}`);
    }
  }

  async toggleTodoCompletion(todoId) {
    // Extract user ID from token and call the correct endpoint
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      // For toggle, we need to first get the current task and then update it
      const currentTask = await this.request(`/users/${userId}/tasks/${todoId}`, {  // baseURL already includes /api/v1
        method: 'GET',
      });

      return this.request(`/users/${userId}/tasks/${todoId}`, {  // baseURL already includes /api/v1
        method: 'PUT',
        body: JSON.stringify({ completed: !currentTask.completed }),
      });
    } catch (error) {
      throw new Error(`Could not toggle todo completion: ${error.message}`);
    }
  }

  // Chat operations
  async getChatHistory() {
    return this.request('/chat/history');  // baseURL already includes /api/v1
  }

  async sendMessage(message) {
    return this.request('/chat/message', {  // baseURL already includes /api/v1
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  // MCP tool calls (mapped to actual backend endpoints)
  async createTodoMCP(title, description = null) {
    // Extract user ID from the token directly instead of calling getUserInfo
    // This avoids the issue with the /users/me endpoint
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      // Decode the JWT token to get the user ID
      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      // Use the correct endpoint path (the baseURL already includes /api/v1)
      const task = await this.request(`/users/${userId}/tasks`, {
        method: 'POST',
        body: JSON.stringify({ title, description }),
      });

      // Return the expected format for MessageHandler
      return {
        success: true,
        todo: task
      };
    } catch (error) {
      // If token decoding fails, re-throw with more context about user not found
      if (error.message.includes('Could not extract user ID') || error.message.includes('No authentication token')) {
        throw new Error('User not found. Please ensure you are logged in and your account exists.');
      }
      // For other errors, return the expected error format
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getTodosMCP(completed = null) {
    // Extract user ID from the token directly instead of calling getUserInfo
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      // Decode the JWT token to get the user ID
      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      // Use the correct endpoint path (the baseURL already includes /api/v1)
      const params = completed !== null ? `?completed=${completed}` : '';
      const response = await this.request(`/users/${userId}/tasks${params}`, {
        method: 'GET',
      });

      // Return the expected format for MessageHandler
      return {
        success: true,
        todos: response.tasks  // The backend returns {tasks: [...], count: n}
      };
    } catch (error) {
      // If token decoding fails, re-throw with more context about user not found
      if (error.message.includes('Could not extract user ID') || error.message.includes('No authentication token')) {
        throw new Error('User not found. Please ensure you are logged in and your account exists.');
      }
      // For other errors, return the expected error format
      return {
        success: false,
        error: error.message
      };
    }
  }

  async updateTodoMCP(todoId, updates) {
    // Extract user ID from the token directly instead of calling getUserInfo
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      // Decode the JWT token to get the user ID
      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      // Use the correct endpoint path (the baseURL already includes /api/v1)
      const task = await this.request(`/users/${userId}/tasks/${todoId}`, {
        method: 'PUT',
        body: JSON.stringify(updates),
      });

      // Return the expected format for MessageHandler
      return {
        success: true,
        todo: task
      };
    } catch (error) {
      // If token decoding fails, re-throw with more context about user not found
      if (error.message.includes('Could not extract user ID') || error.message.includes('No authentication token')) {
        throw new Error('User not found. Please ensure you are logged in and your account exists.');
      }
      // For other errors, return the expected error format
      return {
        success: false,
        error: error.message
      };
    }
  }

  async deleteTodoMCP(todoId) {
    // Extract user ID from the token directly instead of calling getUserInfo
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      // Decode the JWT token to get the user ID
      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      // Use the correct endpoint path (the baseURL already includes /api/v1)
      await this.request(`/users/${userId}/tasks/${todoId}`, {
        method: 'DELETE',
      });

      // Return the expected format for MessageHandler
      return {
        success: true
      };
    } catch (error) {
      // If token decoding fails, re-throw with more context about user not found
      if (error.message.includes('Could not extract user ID') || error.message.includes('No authentication token')) {
        throw new Error('User not found. Please ensure you are logged in and your account exists.');
      }
      // For other errors, return the expected error format
      return {
        success: false,
        error: error.message
      };
    }
  }

  async toggleTodoCompletionMCP(todoId) {
    // Extract user ID from the token directly instead of calling getUserInfo
    try {
      const token = await this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      // Decode the JWT token to get the user ID
      const payload = this.decodeJwtPayload(token);
      const userId = payload.sub;

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      // Use the correct endpoint path (the baseURL already includes /api/v1)
      // First get the current task to see its completion status
      const currentTask = await this.request(`/users/${userId}/tasks/${todoId}`, {
        method: 'GET',
      });

      // Toggle the completed status
      const updatedTask = await this.request(`/users/${userId}/tasks/${todoId}`, {
        method: 'PUT',
        body: JSON.stringify({ completed: !currentTask.completed }),
      });

      // Return the expected format for MessageHandler
      return {
        success: true,
        todo: updatedTask
      };
    } catch (error) {
      // If token decoding fails, re-throw with more context about user not found
      if (error.message.includes('Could not extract user ID') || error.message.includes('No authentication token')) {
        throw new Error('User not found. Please ensure you are logged in and your account exists.');
      }
      // For other errors, return the expected error format
      return {
        success: false,
        error: error.message
      };
    }
  }
}

// Create a singleton instance
const apiService = new ApiService();

export default apiService;