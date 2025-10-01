"use client";

import type React from "react";
import { createContext, useContext, useState, useEffect, useRef } from "react";
import { apiFetch } from "./utils";

interface User {
  id: string;
  email: string;
  username: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (
    username: string,
    email: string,
    password: string
  ) => Promise<{ success: boolean; error?: any }>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_KEY = "token";
const USER_KEY = "user";
const EXPIRY_KEY = "token_expiry";
const SESSION_DURATION = 30 * 60 * 1000; // 30 minutes

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const logoutTimer = useRef<NodeJS.Timeout | null>(null);

  // Restore session on mount
  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    const expiry = localStorage.getItem(EXPIRY_KEY);
    const userData = localStorage.getItem(USER_KEY);

    if (token && expiry && userData) {
      const now = Date.now();
      const expiryTime = parseInt(expiry);

      if (now < expiryTime) {
        const parsedUser: User = JSON.parse(userData);
        setUser(parsedUser);

        // Schedule auto-logout
        scheduleAutoLogout(expiryTime - now);
      } else {
        logout();
      }
    }
    setIsLoading(false);
  }, []);

  const scheduleAutoLogout = (delay: number) => {
    if (logoutTimer.current) clearTimeout(logoutTimer.current);
    logoutTimer.current = setTimeout(() => {
      logout();
      alert("Your session has expired. Please log in again.");
    }, delay);
  };

  const persistSession = (token: string, userData: User) => {
    const expiry = Date.now() + SESSION_DURATION;
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(userData));
    localStorage.setItem(EXPIRY_KEY, expiry.toString());
    setUser(userData);

    // Schedule auto-logout in 30 minutes
    scheduleAutoLogout(SESSION_DURATION);
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await apiFetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const { access_token, user: userData } = response;
      persistSession(access_token, userData);
    } catch (error) {
      console.error("[Logger] Error logging in:", error);
      alert((error as Error).message ?? "Login failed");
    }
  };

  const register = async (username: string, email: string, password: string) => {
    try {
      const response = await apiFetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });
      if (!response) throw new Error("Registration failed");
      const { access_token, user: userData } = response;
      persistSession(access_token, userData);
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error?.body };
    }
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    localStorage.removeItem(EXPIRY_KEY);
    setUser(null);

    if (logoutTimer.current) {
      clearTimeout(logoutTimer.current);
      logoutTimer.current = null;
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
