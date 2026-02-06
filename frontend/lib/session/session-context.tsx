"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface SessionUser {
  id: string;
  email: string;
}

interface SessionContextType {
  user: SessionUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  signOut: () => void;
  refreshSession: () => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export function SessionProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<SessionUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const refreshSession = async () => {
    if (typeof window === "undefined") return;

    const token = localStorage.getItem("auth_token");
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    try {
      // Decode the JWT token to get user info
      const payload = JSON.parse(atob(token.split(".")[1]));
      setUser({
        id: payload.sub,
        email: payload.email,
      });
    } catch (error) {
      // Token is invalid
      localStorage.removeItem("auth_token");
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshSession();
  }, []);

  const signOut = () => {
    localStorage.removeItem("auth_token");
    setUser(null);
  };

  return (
    <SessionContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        signOut,
        refreshSession,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
}

export function useSession() {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error("useSession must be used within a SessionProvider");
  }
  return context;
}
