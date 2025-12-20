/**
 * SAMMO Fight IQ - Authentication Hook
 * Manages user authentication state and token persistence
 */

import { useState, useEffect, useCallback } from 'react';
import { api, User, LoginResponse, RegisterResponse } from '@/lib/api';

// Storage keys
const TOKEN_KEY = 'sammo_auth_token';
const TOKEN_EXPIRY_KEY = 'sammo_auth_expiry';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface UseAuthReturn extends AuthState {
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, password: string, username?: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

/**
 * Custom hook for authentication management
 * Handles login, register, logout, and token persistence in localStorage
 */
export const useAuth = (): UseAuthReturn => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  /**
   * Save token to localStorage with expiry
   */
  const saveToken = useCallback((token: string, expiresIn: number) => {
    const expiryTime = Date.now() + expiresIn * 1000;
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(TOKEN_EXPIRY_KEY, expiryTime.toString());
  }, []);

  /**
   * Remove token from localStorage
   */
  const removeToken = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(TOKEN_EXPIRY_KEY);
  }, []);

  /**
   * Check if token is expired
   */
  const isTokenExpired = useCallback((): boolean => {
    const expiry = localStorage.getItem(TOKEN_EXPIRY_KEY);
    if (!expiry) return true;
    return Date.now() > parseInt(expiry, 10);
  }, []);

  /**
   * Load token from localStorage and fetch user profile
   */
  const loadAuthFromStorage = useCallback(async () => {
    setAuthState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const token = localStorage.getItem(TOKEN_KEY);

      if (!token || isTokenExpired()) {
        removeToken();
        setAuthState({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        });
        return;
      }

      // Fetch user profile to validate token
      const user = await api.getMe(token);

      setAuthState({
        user,
        token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      console.error('Failed to load auth from storage:', error);
      removeToken();
      setAuthState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: 'Session expired. Please login again.',
      });
    }
  }, [isTokenExpired, removeToken]);

  /**
   * Initialize auth state on mount
   */
  useEffect(() => {
    loadAuthFromStorage();
  }, [loadAuthFromStorage]);

  /**
   * Login function
   */
  const login = useCallback(
    async (username: string, password: string): Promise<void> => {
      setAuthState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        const response: LoginResponse = await api.login(username, password);
        const { access_token, expires_in } = response;

        // Save token
        saveToken(access_token, expires_in);

        // Fetch user profile
        const user = await api.getMe(access_token);

        setAuthState({
          user,
          token: access_token,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : 'Login failed';
        setAuthState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));
        throw error;
      }
    },
    [saveToken]
  );

  /**
   * Register function
   */
  const register = useCallback(
    async (
      email: string,
      password: string,
      username?: string
    ): Promise<void> => {
      setAuthState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        const response: RegisterResponse = await api.register(
          email,
          password,
          username
        );

        // After successful registration, login automatically
        const actualUsername = username || email.split('@')[0];
        await login(actualUsername, password);
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : 'Registration failed';
        setAuthState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));
        throw error;
      }
    },
    [login]
  );

  /**
   * Logout function
   */
  const logout = useCallback(() => {
    removeToken();
    setAuthState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
  }, [removeToken]);

  /**
   * Clear error message
   */
  const clearError = useCallback(() => {
    setAuthState((prev) => ({ ...prev, error: null }));
  }, []);

  return {
    ...authState,
    login,
    register,
    logout,
    clearError,
  };
};

export default useAuth;
