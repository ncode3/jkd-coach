/**
 * SAMMO Fight IQ - Dashboard Hook
 * Manages dashboard statistics with auto-refresh
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { api, DashboardStats } from '@/lib/api';

interface UseDashboardState {
  stats: DashboardStats | null;
  isLoading: boolean;
  error: string | null;
}

interface UseDashboardReturn extends UseDashboardState {
  fetchStats: () => Promise<void>;
  clearError: () => void;
  refresh: () => void;
}

const AUTO_REFRESH_INTERVAL = 30000; // 30 seconds

/**
 * Custom hook for dashboard statistics management
 * Automatically refreshes data every 30 seconds
 * @param token - Authentication token
 * @param autoRefresh - Enable/disable auto-refresh (default: true)
 */
export const useDashboard = (
  token: string | null,
  autoRefresh: boolean = true
): UseDashboardReturn => {
  const [state, setState] = useState<UseDashboardState>({
    stats: null,
    isLoading: false,
    error: null,
  });

  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  /**
   * Fetch dashboard statistics from API
   */
  const fetchStats = useCallback(async () => {
    if (!token) {
      setState({
        stats: null,
        isLoading: false,
        error: 'No authentication token provided',
      });
      return;
    }

    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const stats = await api.getDashboardStats(token);
      setState({
        stats,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to fetch dashboard stats';
      console.error('Dashboard fetch error:', error);
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
    }
  }, [token]);

  /**
   * Manual refresh trigger
   */
  const refresh = useCallback(() => {
    fetchStats();
  }, [fetchStats]);

  /**
   * Clear error message
   */
  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  /**
   * Setup auto-refresh interval
   */
  useEffect(() => {
    // Clear any existing interval
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    // Initial fetch
    if (token) {
      fetchStats();

      // Setup auto-refresh if enabled
      if (autoRefresh) {
        intervalRef.current = setInterval(() => {
          fetchStats();
        }, AUTO_REFRESH_INTERVAL);
      }
    }

    // Cleanup on unmount or when dependencies change
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [token, autoRefresh, fetchStats]);

  return {
    ...state,
    fetchStats,
    clearError,
    refresh,
  };
};

export default useDashboard;
