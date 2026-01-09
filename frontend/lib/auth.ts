import { betterAuth } from "better-auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const auth = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
  secret: process.env.BETTER_AUTH_SECRET,
  providers: {
    emailAndPassword: {
      enabled: true,
    },
  },
  advanced: {
    cookiePrefix: "todo-app",
    useSecureCookies: process.env.NODE_ENV === "production",
    crossSubDomainCookies: {
      enabled: false,
    },
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // 5 minutes
    },
  },
  endpoints: {
    signIn: {
      handler: async (ctx: { body: { email: string; password: string } }) => {
        const { email, password } = ctx.body;
        const response = await fetch(`${API_URL}/users/sign-in`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'Sign in failed');
        }

        return {
          user: data.user,
          token: data.token,
        };
      },
    },
    signUp: {
      handler: async (ctx: { body: { email: string; password: string; name: string } }) => {
        const { email, password, name } = ctx.body;
        const response = await fetch(`${API_URL}/users/sign-up`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, name }),
        });
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'Sign up failed');
        }

        return {
          user: data.user,
          token: data.token,
        };
      },
    },
  },
});

