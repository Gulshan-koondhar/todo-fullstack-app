import { getToken } from "./auth-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface FetchOptions extends RequestInit {
  requiresAuth?: boolean;
}

class ApiClient {
  private getAuthHeaders(): HeadersInit {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    // Get JWT token from Better Auth session
    const token = getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    return headers;
  }

  async request<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
    const { requiresAuth = true, headers, ...fetchOptions } = options;

    const url = `${API_URL}${endpoint}`;

    const requestHeaders: HeadersInit = {
      ...(requiresAuth ? this.getAuthHeaders() : {}),
      ...headers,
    };

    const response = await fetch(url, {
      ...fetchOptions,
      headers: requestHeaders,
    });

    // Handle 401 - redirect to signin
    if (response.status === 401 && requiresAuth) {
      if (typeof window !== "undefined") {
        window.location.href = "/signin";
      }
      throw new Error("Unauthorized - redirecting to signin");
    }

    // Handle other error statuses
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}`);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  async get<T>(endpoint: string, requiresAuth = true): Promise<T> {
    return this.request<T>(endpoint, {
      method: "GET",
      requiresAuth,
    });
  }

  async post<T>(endpoint: string, body: unknown, requiresAuth = true): Promise<T> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
      requiresAuth,
    });
  }

  async put<T>(endpoint: string, body: unknown, requiresAuth = true): Promise<T> {
    return this.request<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
      requiresAuth,
    });
  }

  async delete<T>(endpoint: string, requiresAuth = true): Promise<T> {
    return this.request<T>(endpoint, {
      method: "DELETE",
      requiresAuth,
    });
  }
}

export const api = new ApiClient();
