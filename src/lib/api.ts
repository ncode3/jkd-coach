/**
 * SAMMO Fight IQ - API Client
 * Handles all communication with the FastAPI backend
 */

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

// TypeScript Types
export interface User {
  id: string;
  username: string;
  email: string;
  created_at?: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface RegisterResponse {
  status: string;
  user: User;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface RoundData {
  pressure_score: number;
  ring_control_score: number;
  defense_score: number;
  clean_shots_taken: number;
  guard_down_ratio?: number;
  avg_hip_rotation?: number;
  avg_stance_width?: number;
  notes?: string;
}

export interface LogRoundResponse {
  status: string;
  id: string;
  danger_score: number;
  strategy: string;
}

export interface DashboardStats {
  total_rounds: number;
  avg_danger_score: number;
  next_game_plan: string;
  averages?: {
    pressure_score?: number;
    ring_control_score?: number;
    defense_score?: number;
    danger_score?: number;
  };
  most_recent_round_date?: string;
}

export interface Round {
  id: string;
  user_id: string;
  pressure_score: number;
  ring_control_score: number;
  defense_score: number;
  clean_shots_taken: number;
  guard_down_ratio?: number;
  avg_hip_rotation?: number;
  avg_stance_width?: number;
  danger_score: number;
  strategy?: string;
  notes?: string;
  created_at: string;
}

export interface RoundsHistoryResponse {
  rounds: Round[];
  total: number;
}

export interface DeleteRoundResponse {
  status: string;
  message: string;
}

export interface ApiError {
  detail: string;
}

// Helper function to handle API errors
const handleResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const errorData: ApiError = await response.json().catch(() => ({
      detail: `HTTP error! status: ${response.status}`,
    }));
    throw new Error(errorData.detail || 'An error occurred');
  }
  return response.json();
};

// API Client Class
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Register a new user
   */
  async register(
    email: string,
    password: string,
    username?: string
  ): Promise<RegisterResponse> {
    const response = await fetch(`${this.baseUrl}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username || email.split('@')[0],
        email,
        password,
      }),
    });

    return handleResponse<RegisterResponse>(response);
  }

  /**
   * Login with username and password
   */
  async login(username: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    return handleResponse<LoginResponse>(response);
  }

  /**
   * Get current user profile
   */
  async getMe(token: string): Promise<User> {
    const response = await fetch(`${this.baseUrl}/auth/me`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return handleResponse<User>(response);
  }

  /**
   * Log a new round with boxing metrics
   */
  async logRound(token: string, roundData: RoundData): Promise<LogRoundResponse> {
    const response = await fetch(`${this.baseUrl}/api/log_round`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(roundData),
    });

    return handleResponse<LogRoundResponse>(response);
  }

  /**
   * Get dashboard statistics
   */
  async getDashboardStats(token: string): Promise<DashboardStats> {
    const response = await fetch(`${this.baseUrl}/api/dashboard_stats`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return handleResponse<DashboardStats>(response);
  }

  /**
   * Get rounds history with optional limit
   */
  async getRoundsHistory(token: string, limit: number = 100): Promise<RoundsHistoryResponse> {
    const response = await fetch(
      `${this.baseUrl}/api/rounds_history?limit=${limit}`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return handleResponse<RoundsHistoryResponse>(response);
  }

  /**
   * Delete a round by ID
   */
  async deleteRound(token: string, roundId: string): Promise<DeleteRoundResponse> {
    const response = await fetch(`${this.baseUrl}/api/rounds/${roundId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return handleResponse<DeleteRoundResponse>(response);
  }

  /**
   * Upload video for future pose detection integration
   */
  async uploadVideo(token: string, videoFile: File): Promise<any> {
    const formData = new FormData();
    formData.append('video', videoFile);

    const response = await fetch(`${this.baseUrl}/api/upload_video`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });

    return handleResponse<any>(response);
  }
}

// Export singleton instance
export const api = new ApiClient();

// Export default
export default api;
