import React, { createContext, ReactNode, useContext, useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { apiService } from '../services/api';
import { LoginResponse, User } from '../types';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => void;
  updateUser: (userData: any) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('fins_token');
      const userData = localStorage.getItem('fins_user');

      if (token && userData) {
        try {
          const currentUser = await apiService.getCurrentUser();
          setUser(currentUser);
        } catch (error) {
          console.error('Erro ao verificar usuário:', error);
          localStorage.removeItem('fins_token');
          localStorage.removeItem('fins_user');
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      const response: LoginResponse = await apiService.login(email, password);
      
      localStorage.setItem('fins_token', response.access_token);
      localStorage.setItem('fins_user', JSON.stringify(response.user));
      
      const currentUser = await apiService.getCurrentUser();
      setUser(currentUser);
      
      toast.success('Login realizado com sucesso!');
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Erro ao fazer login';
      toast.error(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData: any) => {
    try {
      setLoading(true);
      await apiService.register(userData);
      toast.success('Conta criada com sucesso! Faça login para continuar.');
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Erro ao criar conta';
      toast.error(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('fins_token');
    localStorage.removeItem('fins_user');
    setUser(null);
    toast.success('Logout realizado com sucesso!');
  };

  const updateUser = async (userData: any) => {
    try {
      setLoading(true);
      const updatedUser = await apiService.updateUser(userData);
      setUser(updatedUser);
      localStorage.setItem('fins_user', JSON.stringify(updatedUser));
      toast.success('Perfil atualizado com sucesso!');
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Erro ao atualizar perfil';
      toast.error(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 