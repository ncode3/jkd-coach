/**
 * SAMMO Fight IQ - Type Definitions
 * Centralized TypeScript types for the application
 */

// Re-export all types from API for convenience
export type {
  User,
  RegisterRequest,
  RegisterResponse,
  LoginRequest,
  LoginResponse,
  RoundData,
  LogRoundResponse,
  DashboardStats,
  Round,
  RoundsHistoryResponse,
  DeleteRoundResponse,
  ApiError,
} from '@/lib/api';

// Additional UI-specific types can be added here

export interface UIState {
  isLoading: boolean;
  error: string | null;
}

export interface PaginationState {
  page: number;
  limit: number;
  total: number;
}

export type DangerLevel = 'low' | 'moderate' | 'high' | 'critical';

export interface DangerScoreThresholds {
  low: number;
  moderate: number;
  high: number;
}
