/**
 * HTTP client for API requests with JWT authentication.
 */

import { tokenStorage } from './tokenStorage';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_V1_URL = `${API_BASE_URL}/api/v1`;

export interface ApiError {
    message: string;
    status?: number;
}

class ApiClient {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    /**
     * Make an HTTP request with automatic token injection.
     */
    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;
        const token = tokenStorage.getToken();

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        // Add authorization header if token exists
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers,
            });

            // Handle 204 No Content
            if (response.status === 204) {
                return undefined as T;
            }

            // Parse JSON response
            const data = await response.json();

            // Handle error responses
            if (!response.ok) {
                const error: ApiError = {
                    message: data.detail || data.error || 'An error occurred',
                    status: response.status,
                };
                throw error;
            }

            return data;
        } catch (error) {
            if (error instanceof Error && 'status' in error) {
                throw error;
            }
            throw {
                message: error instanceof Error ? error.message : 'Network error',
            } as ApiError;
        }
    }

    /**
     * GET request.
     */
    async get<T>(endpoint: string): Promise<T> {
        return this.request<T>(endpoint, { method: 'GET' });
    }

    /**
     * POST request with JSON body.
     */
    async post<T>(endpoint: string, body?: unknown): Promise<T> {
        return this.request<T>(endpoint, {
            method: 'POST',
            body: body ? JSON.stringify(body) : undefined,
        });
    }

    /**
     * POST request with form data (for OAuth2).
     */
    async postForm<T>(endpoint: string, data: Record<string, string>): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;
        const token = tokenStorage.getToken();

        const formData = new URLSearchParams();
        Object.entries(data).forEach(([key, value]) => {
            formData.append(key, value);
        });

        const headers: HeadersInit = {
            'Content-Type': 'application/x-www-form-urlencoded',
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers,
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                const error: ApiError = {
                    message: data.detail || data.error || 'An error occurred',
                    status: response.status,
                };
                throw error;
            }

            return data;
        } catch (error) {
            if (error instanceof Error && 'status' in error) {
                throw error;
            }
            throw {
                message: error instanceof Error ? error.message : 'Network error',
            } as ApiError;
        }
    }
}

export const apiClient = new ApiClient(API_V1_URL);
export { API_BASE_URL, API_V1_URL };
