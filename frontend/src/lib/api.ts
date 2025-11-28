import { User, LeaderboardEntry, ActivePlayer, GameMode } from '@/types/game';
import { createInitialState } from './gameLogic';

// Simulated delay for mock API calls
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Mock data storage
let currentUser: User | null = null;

const mockUsers: Map<string, { user: User; password: string }> = new Map([
  ['demo@snake.game', { user: { id: '1', username: 'DemoPlayer', email: 'demo@snake.game' }, password: 'demo123' }],
]);

const mockLeaderboard: LeaderboardEntry[] = [
  { id: '1', username: 'SnakeMaster', score: 2450, mode: 'walls', date: '2024-01-15' },
  { id: '2', username: 'PyThonKing', score: 2180, mode: 'pass-through', date: '2024-01-14' },
  { id: '3', username: 'NeonViper', score: 1920, mode: 'walls', date: '2024-01-14' },
  { id: '4', username: 'PixelSnake', score: 1750, mode: 'pass-through', date: '2024-01-13' },
  { id: '5', username: 'RetroGamer', score: 1680, mode: 'walls', date: '2024-01-13' },
  { id: '6', username: 'ArcadeLegend', score: 1540, mode: 'pass-through', date: '2024-01-12' },
  { id: '7', username: 'GridRunner', score: 1420, mode: 'walls', date: '2024-01-12' },
  { id: '8', username: 'CobraCommand', score: 1350, mode: 'pass-through', date: '2024-01-11' },
  { id: '9', username: 'SlitherPro', score: 1280, mode: 'walls', date: '2024-01-11' },
  { id: '10', username: 'BinarySnake', score: 1150, mode: 'pass-through', date: '2024-01-10' },
];

const mockActivePlayers: ActivePlayer[] = [
  { id: 'ap1', username: 'LivePlayer1', score: 340, mode: 'walls', gameState: createInitialState('walls') },
  { id: 'ap2', username: 'LivePlayer2', score: 520, mode: 'pass-through', gameState: createInitialState('pass-through') },
  { id: 'ap3', username: 'ProSnaker', score: 780, mode: 'walls', gameState: createInitialState('walls') },
];

// Auth API
export const api = {
  auth: {
    login: async (email: string, password: string): Promise<{ success: boolean; user?: User; error?: string }> => {
      await delay(500);
      const userData = mockUsers.get(email);
      if (!userData) {
        return { success: false, error: 'User not found' };
      }
      if (userData.password !== password) {
        return { success: false, error: 'Invalid password' };
      }
      currentUser = userData.user;
      return { success: true, user: userData.user };
    },

    signup: async (email: string, username: string, password: string): Promise<{ success: boolean; user?: User; error?: string }> => {
      await delay(500);
      if (mockUsers.has(email)) {
        return { success: false, error: 'Email already registered' };
      }
      const newUser: User = {
        id: String(mockUsers.size + 1),
        username,
        email,
      };
      mockUsers.set(email, { user: newUser, password });
      currentUser = newUser;
      return { success: true, user: newUser };
    },

    logout: async (): Promise<void> => {
      await delay(200);
      currentUser = null;
    },

    getCurrentUser: async (): Promise<User | null> => {
      await delay(100);
      return currentUser;
    },
  },

  leaderboard: {
    getAll: async (mode?: GameMode): Promise<LeaderboardEntry[]> => {
      await delay(300);
      if (mode) {
        return mockLeaderboard.filter(entry => entry.mode === mode);
      }
      return mockLeaderboard;
    },

    submitScore: async (score: number, mode: GameMode): Promise<{ success: boolean; rank?: number }> => {
      await delay(300);
      if (!currentUser) {
        return { success: false };
      }
      const newEntry: LeaderboardEntry = {
        id: String(mockLeaderboard.length + 1),
        username: currentUser.username,
        score,
        mode,
        date: new Date().toISOString().split('T')[0],
      };
      mockLeaderboard.push(newEntry);
      mockLeaderboard.sort((a, b) => b.score - a.score);
      const rank = mockLeaderboard.findIndex(e => e.id === newEntry.id) + 1;
      return { success: true, rank };
    },
  },

  spectate: {
    getActivePlayers: async (): Promise<ActivePlayer[]> => {
      await delay(300);
      return mockActivePlayers;
    },

    getPlayerGameState: async (playerId: string): Promise<ActivePlayer | null> => {
      await delay(100);
      return mockActivePlayers.find(p => p.id === playerId) || null;
    },
  },
};

export default api;
