import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { User, AuthState } from '@/types/game';
import api from '@/lib/api';

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  signup: (email: string, username: string, password: string) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
  });

  useEffect(() => {
    const checkAuth = async () => {
      const user = await api.auth.getCurrentUser();
      setState({
        user,
        isAuthenticated: !!user,
        isLoading: false,
      });
    };
    checkAuth();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    setState(prev => ({ ...prev, isLoading: true }));
    const result = await api.auth.login(email, password);
    if (result.success && result.user) {
      setState({
        user: result.user,
        isAuthenticated: true,
        isLoading: false,
      });
      return { success: true };
    }
    setState(prev => ({ ...prev, isLoading: false }));
    return { success: false, error: result.error };
  }, []);

  const signup = useCallback(async (email: string, username: string, password: string) => {
    setState(prev => ({ ...prev, isLoading: true }));
    const result = await api.auth.signup(email, username, password);
    if (result.success && result.user) {
      setState({
        user: result.user,
        isAuthenticated: true,
        isLoading: false,
      });
      return { success: true };
    }
    setState(prev => ({ ...prev, isLoading: false }));
    return { success: false, error: result.error };
  }, []);

  const logout = useCallback(async () => {
    await api.auth.logout();
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
    });
  }, []);

  return (
    <AuthContext.Provider value={{ ...state, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
