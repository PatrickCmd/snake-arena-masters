import { User, LeaderboardEntry, ActivePlayer, GameMode, Token } from '@/types/game';
import { apiClient, ApiError } from './apiClient';
import { tokenStorage } from './tokenStorage';

// Auth API
export const api = {
  auth: {
    login: async (
      email: string,
      password: string
    ): Promise<{ success: boolean; user?: User; error?: string }> => {
      try {
        // Login with OAuth2 form data
        const tokenResponse = await apiClient.postForm<Token>('/auth/login', {
          username: email, // OAuth2 uses 'username' field for email
          password,
        });

        // Store the token
        tokenStorage.setToken(tokenResponse.access_token);

        // Get user data
        const user = await apiClient.get<User>('/auth/me');

        return { success: true, user };
      } catch (error) {
        const apiError = error as ApiError;
        return { success: false, error: apiError.message };
      }
    },

    signup: async (
      email: string,
      username: string,
      password: string
    ): Promise<{ success: boolean; user?: User; error?: string }> => {
      try {
        const response = await apiClient.post<{ success: boolean; user?: User; error?: string }>(
          '/auth/signup',
          { email, username, password }
        );

        if (response.success && response.user) {
          // Auto-login after signup
          const loginResult = await api.auth.login(email, password);
          return loginResult;
        }

        return response;
      } catch (error) {
        const apiError = error as ApiError;
        return { success: false, error: apiError.message };
      }
    },

    logout: async (): Promise<void> => {
      try {
        await apiClient.post('/auth/logout');
      } catch (error) {
        // Ignore logout errors
        console.error('Logout error:', error);
      } finally {
        // Always clear token
        tokenStorage.clearToken();
      }
    },

    getCurrentUser: async (): Promise<User | null> => {
      try {
        if (!tokenStorage.hasToken()) {
          return null;
        }
        const user = await apiClient.get<User>('/auth/me');
        return user;
      } catch (error) {
        // If token is invalid, clear it
        tokenStorage.clearToken();
        return null;
      }
    },
  },

  leaderboard: {
    getAll: async (mode?: GameMode): Promise<LeaderboardEntry[]> => {
      try {
        const endpoint = mode ? `/leaderboard?mode=${mode}` : '/leaderboard';
        const entries = await apiClient.get<LeaderboardEntry[]>(endpoint);
        return entries;
      } catch (error) {
        console.error('Failed to fetch leaderboard:', error);
        return [];
      }
    },

    submitScore: async (
      score: number,
      mode: GameMode
    ): Promise<{ success: boolean; rank?: number; error?: string }> => {
      try {
        const response = await apiClient.post<{ success: boolean; rank?: number; error?: string }>(
          '/leaderboard/scores',
          { score, mode }
        );
        return response;
      } catch (error) {
        const apiError = error as ApiError;
        return { success: false, error: apiError.message };
      }
    },

    getBestScore: async (mode: GameMode): Promise<number | null> => {
      try {
        const score = await apiClient.get<number | null>(`/leaderboard/best-score/${mode}`);
        return score;
      } catch (error) {
        console.error('Failed to fetch best score:', error);
        return null;
      }
    },
  },

  spectate: {
    getActivePlayers: async (): Promise<ActivePlayer[]> => {
      try {
        const players = await apiClient.get<ActivePlayer[]>('/spectate/players');
        return players;
      } catch (error) {
        console.error('Failed to fetch active players:', error);
        return [];
      }
    },

    getPlayerGameState: async (playerId: string): Promise<ActivePlayer | null> => {
      try {
        const player = await apiClient.get<ActivePlayer>(`/spectate/players/${playerId}`);
        return player;
      } catch (error) {
        console.error('Failed to fetch player game state:', error);
        return null;
      }
    },
  },
};

export default api;
