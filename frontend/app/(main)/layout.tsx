"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "@/lib/session/session-context";
import { Button } from "@/components/ui/button";
import { Moon, Sun, LogOut } from "lucide-react";
import { useTheme } from "next-themes";
import FloatingChatButton from "@/components/chat/FloatingChatButton";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { theme, setTheme } = useTheme();
  const { isAuthenticated, isLoading: sessionLoading, signOut, user } = useSession();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!sessionLoading) {
      if (!isAuthenticated) {
        router.push("/signin");
      } else {
        setIsLoading(false);
      }
    }
  }, [isAuthenticated, sessionLoading, router]);

  const handleSignOut = () => {
    signOut();
    router.push("/signin");
  };

  if (isLoading || sessionLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto" />
          <p className="mt-2 text-sm text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <h1 className="text-xl font-semibold">My Tasks</h1>
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground mr-2">{user?.email}</span>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              aria-label="Toggle theme"
            >
              <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleSignOut}
              aria-label="Sign out"
            >
              <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">{children}</main>
      <FloatingChatButton />
    </div>
  );
}
