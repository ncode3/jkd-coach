/**
 * SAMMO Fight IQ - Rounds Management Hook
 * Manages rounds history with optimistic updates
 */

import { useState, useEffect, useCallback } from 'react';
import { api, Round, RoundData, RoundsHistoryResponse, LogRoundResponse } from '@/lib/api';

interface UseRoundsState {
  rounds: Round[];
  total: number;
  isLoading: boolean;
  error: string | null;
  isSubmitting: boolean;
}

interface UseRoundsReturn extends UseRoundsState {
  fetchHistory: (limit?: number) => Promise<void>;
  logRound: (roundData: RoundData) => Promise<LogRoundResponse>;
  deleteRound: (roundId: string) => Promise<void>;
  clearError: () => void;
  refresh: () => void;
}

/**
 * Custom hook for rounds management
 * Handles fetching, logging, and deleting rounds with optimistic updates
 * @param token - Authentication token
 * @param autoLoad - Automatically load rounds on mount (default: true)
 */
export const useRounds = (
  token: string | null,
  autoLoad: boolean = true
): UseRoundsReturn => {
  const [state, setState] = useState<UseRoundsState>({
    rounds: [],
    total: 0,
    isLoading: false,
    error: null,
    isSubmitting: false,
  });

  /**
   * Fetch rounds history from API
   */
  const fetchHistory = useCallback(
    async (limit: number = 100): Promise<void> => {
      if (!token) {
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: 'No authentication token provided',
        }));
        return;
      }

      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        const response: RoundsHistoryResponse = await api.getRoundsHistory(
          token,
          limit
        );
        setState({
          rounds: response.rounds,
          total: response.total,
          isLoading: false,
          error: null,
          isSubmitting: false,
        });
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : 'Failed to fetch rounds history';
        console.error('Rounds fetch error:', error);
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));
      }
    },
    [token]
  );

  /**
   * Log a new round with optimistic update
   */
  const logRound = useCallback(
    async (roundData: RoundData): Promise<LogRoundResponse> => {
      if (!token) {
        throw new Error('No authentication token provided');
      }

      setState((prev) => ({ ...prev, isSubmitting: true, error: null }));

      try {
        const response: LogRoundResponse = await api.logRound(token, roundData);

        // Create optimistic round object
        const optimisticRound: Round = {
          id: response.id,
          user_id: '', // Will be populated on next fetch
          pressure_score: roundData.pressure_score,
          ring_control_score: roundData.ring_control_score,
          defense_score: roundData.defense_score,
          clean_shots_taken: roundData.clean_shots_taken,
          guard_down_ratio: roundData.guard_down_ratio,
          avg_hip_rotation: roundData.avg_hip_rotation,
          avg_stance_width: roundData.avg_stance_width,
          danger_score: response.danger_score,
          strategy: response.strategy,
          notes: roundData.notes,
          created_at: new Date().toISOString(),
        };

        // Optimistic update: add new round to the beginning of the list
        setState((prev) => ({
          ...prev,
          rounds: [optimisticRound, ...prev.rounds],
          total: prev.total + 1,
          isSubmitting: false,
          error: null,
        }));

        // Fetch fresh data in the background to ensure consistency
        fetchHistory();

        return response;
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : 'Failed to log round';
        console.error('Log round error:', error);
        setState((prev) => ({
          ...prev,
          isSubmitting: false,
          error: errorMessage,
        }));
        throw error;
      }
    },
    [token, fetchHistory]
  );

  /**
   * Delete a round with optimistic update
   */
  const deleteRound = useCallback(
    async (roundId: string): Promise<void> => {
      if (!token) {
        throw new Error('No authentication token provided');
      }

      // Store original rounds for rollback on error
      const originalRounds = state.rounds;
      const originalTotal = state.total;

      // Optimistic update: remove round immediately
      setState((prev) => ({
        ...prev,
        rounds: prev.rounds.filter((round) => round.id !== roundId),
        total: prev.total - 1,
        error: null,
      }));

      try {
        await api.deleteRound(token, roundId);

        // Fetch fresh data to ensure consistency
        fetchHistory();
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : 'Failed to delete round';
        console.error('Delete round error:', error);

        // Rollback on error
        setState((prev) => ({
          ...prev,
          rounds: originalRounds,
          total: originalTotal,
          error: errorMessage,
        }));
        throw error;
      }
    },
    [token, state.rounds, state.total, fetchHistory]
  );

  /**
   * Manual refresh trigger
   */
  const refresh = useCallback(() => {
    fetchHistory();
  }, [fetchHistory]);

  /**
   * Clear error message
   */
  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  /**
   * Auto-load rounds on mount if enabled
   */
  useEffect(() => {
    if (token && autoLoad) {
      fetchHistory();
    }
  }, [token, autoLoad, fetchHistory]);

  return {
    ...state,
    fetchHistory,
    logRound,
    deleteRound,
    clearError,
    refresh,
  };
};

export default useRounds;
