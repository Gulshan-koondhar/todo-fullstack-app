import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
});

// Helper to get JWT token for API calls
export function getToken(): string | null {
  if (typeof window === "undefined") return null;

  // First try to get from localStorage (our custom auth)
  const localToken = localStorage.getItem('auth_token');
  if (localToken) {
    return localToken;
  }

  // Fallback to Better Auth cookies
  const cookies = document.cookie.split("; ");
  const sessionCookie = cookies.find((c) =>
    c.startsWith("todo-app_session_token=")
  );

  if (sessionCookie) {
    return sessionCookie.substring("todo-app_session_token=".length);
  }

  return null;
}

// Re-export auth functions from the client
export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient;
