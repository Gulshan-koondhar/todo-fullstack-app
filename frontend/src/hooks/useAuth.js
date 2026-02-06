import { useState, useEffect, createContext, useContext } from 'react';
import { useRouter } from 'next/router';

// Create authentication context
const AuthContext = createContext();

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Check if user is logged in on component mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        if (token) {
          // Verify token with backend
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user`, {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });

          if (response.ok) {
            const userData = await response.json();
            setUser({ id: userData.user_id });
          } else {
            // Token is invalid, remove it
            localStorage.removeItem('auth_token');
          }
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        localStorage.removeItem('auth_token');
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  // Login function
  const login = async (email, password) => {
    try {
      // In a real app, this would be a proper login endpoint
      // For now, we'll simulate login with a dummy token
      const response = await fetch(`${process.env.NEXT_PUBLIC_BETTER_AUTH_URL}/api/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const token = data.token; // Assuming the response contains a token
        localStorage.setItem('auth_token', token);
        setUser({ id: data.user_id });
        router.push('/dashboard'); // Redirect to dashboard after login
        return { success: true };
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.message || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error' };
    }
  };

  // Signup function
  const signup = async (email, password, name) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BETTER_AUTH_URL}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (response.ok) {
        const data = await response.json();
        const token = data.token; // Assuming the response contains a token
        localStorage.setItem('auth_token', token);
        setUser({ id: data.user_id });
        router.push('/dashboard'); // Redirect to dashboard after signup
        return { success: true };
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.message || 'Signup failed' };
      }
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: 'Network error' };
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
    router.push('/'); // Redirect to home after logout
  };

  // Check if user is authenticated
  const isAuthenticated = () => {
    return !!user;
  };

  // Get auth token
  const getAuthToken = () => {
    return localStorage.getItem('auth_token');
  };

  const value = {
    user,
    login,
    signup,
    logout,
    loading,
    isAuthenticated,
    getAuthToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};