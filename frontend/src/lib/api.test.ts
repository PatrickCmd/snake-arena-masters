import { describe, it, expect, beforeEach, vi, Mock } from 'vitest';
import api from './api';
import { apiClient } from './apiClient';
import { tokenStorage } from './tokenStorage';

// Mock dependencies
vi.mock('./apiClient', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    postForm: vi.fn(),
  },
}));

vi.mock('./tokenStorage', () => ({
  tokenStorage: {
    getToken: vi.fn(),
    setToken: vi.fn(),
    clearToken: vi.fn(),
    hasToken: vi.fn(),
  },
}));

describe('Auth API', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('login', () => {
    it('should login with valid credentials', async () => {
      const mockToken = { access_token: 'fake-token', token_type: 'bearer' };
      const mockUser = { id: '1', username: 'DemoPlayer', email: 'demo@snake.game' };

      (apiClient.postForm as Mock).mockResolvedValue(mockToken);
      (apiClient.get as Mock).mockResolvedValue(mockUser);

      const result = await api.auth.login('demo@snake.game', 'demo123');

      expect(apiClient.postForm).toHaveBeenCalledWith('/auth/login', {
        username: 'demo@snake.game',
        password: 'demo123',
      });
      expect(tokenStorage.setToken).toHaveBeenCalledWith('fake-token');
      expect(apiClient.get).toHaveBeenCalledWith('/auth/me');
      expect(result.success).toBe(true);
      expect(result.user).toEqual(mockUser);
    });

    it('should fail with invalid credentials', async () => {
      (apiClient.postForm as Mock).mockRejectedValue({ message: 'Invalid credentials' });

      const result = await api.auth.login('invalid@email.com', 'password');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid credentials');
    });
  });

  describe('signup', () => {
    it('should create new account and auto-login', async () => {
      const mockUser = { id: '2', username: 'NewUser', email: 'new@test.com' };
      const mockToken = { access_token: 'fake-token', token_type: 'bearer' };

      // Mock signup success
      (apiClient.post as Mock).mockResolvedValue({ success: true, user: mockUser });
      // Mock login success (auto-login)
      (apiClient.postForm as Mock).mockResolvedValue(mockToken);
      (apiClient.get as Mock).mockResolvedValue(mockUser);

      const result = await api.auth.signup('new@test.com', 'NewUser', 'pass123');

      expect(apiClient.post).toHaveBeenCalledWith('/auth/signup', {
        email: 'new@test.com',
        username: 'NewUser',
        password: 'pass123',
      });
      expect(apiClient.postForm).toHaveBeenCalled(); // Auto-login
      expect(result.success).toBe(true);
      expect(result.user).toEqual(mockUser);
    });

    it('should fail with existing email', async () => {
      (apiClient.post as Mock).mockRejectedValue({ message: 'Email already registered' });

      const result = await api.auth.signup('existing@test.com', 'User', 'pass');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Email already registered');
    });
  });

  describe('getCurrentUser', () => {
    it('should return null when no token exists', async () => {
      (tokenStorage.hasToken as Mock).mockReturnValue(false);

      const user = await api.auth.getCurrentUser();

      expect(user).toBeNull();
      expect(apiClient.get).not.toHaveBeenCalled();
    });

    it('should return user when token exists', async () => {
      const mockUser = { id: '1', username: 'User', email: 'user@test.com' };
      (tokenStorage.hasToken as Mock).mockReturnValue(true);
      (apiClient.get as Mock).mockResolvedValue(mockUser);

      const user = await api.auth.getCurrentUser();

      expect(user).toEqual(mockUser);
    });

    it('should clear token on error', async () => {
      (tokenStorage.hasToken as Mock).mockReturnValue(true);
      (apiClient.get as Mock).mockRejectedValue(new Error('Invalid token'));

      const user = await api.auth.getCurrentUser();

      expect(user).toBeNull();
      expect(tokenStorage.clearToken).toHaveBeenCalled();
    });
  });

  describe('logout', () => {
    it('should call logout endpoint and clear token', async () => {
      (apiClient.post as Mock).mockResolvedValue({});

      await api.auth.logout();

      expect(apiClient.post).toHaveBeenCalledWith('/auth/logout');
      expect(tokenStorage.clearToken).toHaveBeenCalled();
    });
  });
});

describe('Leaderboard API', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getAll', () => {
    it('should fetch leaderboard entries', async () => {
      const mockEntries = [{ id: '1', username: 'User', score: 100, mode: 'walls' }];
      (apiClient.get as Mock).mockResolvedValue(mockEntries);

      const entries = await api.leaderboard.getAll();

      expect(apiClient.get).toHaveBeenCalledWith('/leaderboard');
      expect(entries).toEqual(mockEntries);
    });

    it('should fetch filtered leaderboard', async () => {
      await api.leaderboard.getAll('walls');
      expect(apiClient.get).toHaveBeenCalledWith('/leaderboard?mode=walls');
    });
  });

  describe('submitScore', () => {
    it('should submit score successfully', async () => {
      (apiClient.post as Mock).mockResolvedValue({ success: true, rank: 5 });

      const result = await api.leaderboard.submitScore(100, 'walls');

      expect(apiClient.post).toHaveBeenCalledWith('/leaderboard/scores', {
        score: 100,
        mode: 'walls',
      });
      expect(result.success).toBe(true);
      expect(result.rank).toBe(5);
    });

    it('should handle errors', async () => {
      (apiClient.post as Mock).mockRejectedValue({ message: 'Error' });

      const result = await api.leaderboard.submitScore(100, 'walls');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Error');
    });
  });
});

describe('Spectate API', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getActivePlayers', () => {
    it('should fetch active players', async () => {
      const mockPlayers = [{ id: '1', username: 'Player' }];
      (apiClient.get as Mock).mockResolvedValue(mockPlayers);

      const players = await api.spectate.getActivePlayers();

      expect(apiClient.get).toHaveBeenCalledWith('/spectate/players');
      expect(players).toEqual(mockPlayers);
    });
  });

  describe('getPlayerGameState', () => {
    it('should fetch player game state', async () => {
      const mockPlayer = { id: '1', username: 'Player', gameState: {} };
      (apiClient.get as Mock).mockResolvedValue(mockPlayer);

      const player = await api.spectate.getPlayerGameState('1');

      expect(apiClient.get).toHaveBeenCalledWith('/spectate/players/1');
      expect(player).toEqual(mockPlayer);
    });

    it('should return null on error', async () => {
      (apiClient.get as Mock).mockRejectedValue(new Error('Not found'));

      const player = await api.spectate.getPlayerGameState('1');

      expect(player).toBeNull();
    });
  });
});
