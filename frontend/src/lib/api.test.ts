import { describe, it, expect, beforeEach } from 'vitest';
import api from './api';

describe('Auth API', () => {
  beforeEach(async () => {
    // Logout before each test to ensure clean state
    await api.auth.logout();
  });

  describe('login', () => {
    it('should login with valid credentials', async () => {
      const result = await api.auth.login('demo@snake.game', 'demo123');
      expect(result.success).toBe(true);
      expect(result.user).toBeDefined();
      expect(result.user?.username).toBe('DemoPlayer');
    });

    it('should fail with invalid email', async () => {
      const result = await api.auth.login('invalid@email.com', 'password');
      expect(result.success).toBe(false);
      expect(result.error).toBe('User not found');
    });

    it('should fail with invalid password', async () => {
      const result = await api.auth.login('demo@snake.game', 'wrongpassword');
      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid password');
    });
  });

  describe('signup', () => {
    it('should create new account with valid data', async () => {
      const result = await api.auth.signup('newuser@test.com', 'NewUser', 'password123');
      expect(result.success).toBe(true);
      expect(result.user).toBeDefined();
      expect(result.user?.username).toBe('NewUser');
      expect(result.user?.email).toBe('newuser@test.com');
    });

    it('should fail with existing email', async () => {
      const result = await api.auth.signup('demo@snake.game', 'AnotherUser', 'password');
      expect(result.success).toBe(false);
      expect(result.error).toBe('Email already registered');
    });
  });

  describe('getCurrentUser', () => {
    it('should return null when not logged in', async () => {
      const user = await api.auth.getCurrentUser();
      expect(user).toBeNull();
    });

    it('should return user when logged in', async () => {
      await api.auth.login('demo@snake.game', 'demo123');
      const user = await api.auth.getCurrentUser();
      expect(user).not.toBeNull();
      expect(user?.email).toBe('demo@snake.game');
    });
  });

  describe('logout', () => {
    it('should clear current user', async () => {
      await api.auth.login('demo@snake.game', 'demo123');
      await api.auth.logout();
      const user = await api.auth.getCurrentUser();
      expect(user).toBeNull();
    });
  });
});

describe('Leaderboard API', () => {
  describe('getAll', () => {
    it('should return all leaderboard entries', async () => {
      const entries = await api.leaderboard.getAll();
      expect(entries.length).toBeGreaterThan(0);
    });

    it('should filter by mode when specified', async () => {
      const wallsEntries = await api.leaderboard.getAll('walls');
      expect(wallsEntries.every(e => e.mode === 'walls')).toBe(true);

      const passThroughEntries = await api.leaderboard.getAll('pass-through');
      expect(passThroughEntries.every(e => e.mode === 'pass-through')).toBe(true);
    });
  });

  describe('submitScore', () => {
    beforeEach(async () => {
      await api.auth.logout();
    });

    it('should fail when not authenticated', async () => {
      const result = await api.leaderboard.submitScore(1000, 'walls');
      expect(result.success).toBe(false);
    });

    it('should succeed when authenticated', async () => {
      await api.auth.login('demo@snake.game', 'demo123');
      const result = await api.leaderboard.submitScore(1000, 'walls');
      expect(result.success).toBe(true);
      expect(result.rank).toBeDefined();
    });
  });
});

describe('Spectate API', () => {
  describe('getActivePlayers', () => {
    it('should return active players', async () => {
      const players = await api.spectate.getActivePlayers();
      expect(players.length).toBeGreaterThan(0);
      expect(players[0]).toHaveProperty('id');
      expect(players[0]).toHaveProperty('username');
      expect(players[0]).toHaveProperty('score');
      expect(players[0]).toHaveProperty('mode');
      expect(players[0]).toHaveProperty('gameState');
    });
  });

  describe('getPlayerGameState', () => {
    it('should return player game state for valid id', async () => {
      const players = await api.spectate.getActivePlayers();
      const player = await api.spectate.getPlayerGameState(players[0].id);
      expect(player).not.toBeNull();
      expect(player?.id).toBe(players[0].id);
    });

    it('should return null for invalid id', async () => {
      const player = await api.spectate.getPlayerGameState('invalid-id');
      expect(player).toBeNull();
    });
  });
});
