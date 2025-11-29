/**
 * Token storage utilities for managing JWT tokens.
 */

const TOKEN_KEY = 'snake_arena_token';

export const tokenStorage = {
    /**
     * Get the stored JWT token.
     */
    getToken(): string | null {
        return localStorage.getItem(TOKEN_KEY);
    },

    /**
     * Store a JWT token.
     */
    setToken(token: string): void {
        localStorage.setItem(TOKEN_KEY, token);
    },

    /**
     * Remove the stored token.
     */
    clearToken(): void {
        localStorage.removeItem(TOKEN_KEY);
    },

    /**
     * Check if a token exists.
     */
    hasToken(): boolean {
        return this.getToken() !== null;
    },
};
