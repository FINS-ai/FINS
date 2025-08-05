import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
    BalancePrediction,
    Expense,
    ExpenseAnalysis,
    ExpenseCreate,
    ExpenseUpdate,
    FinancialInsights,
    FinancialProfile,
    FinancialProfileCreate,
    FinancialProfileUpdate,
    FinancialSummary,
    LoginResponse,
    Receipt,
    ReceiptCreate,
    RiskAnalysis,
    SavingsPrediction,
    User,
    UserCreate,
    UserUpdate,
} from '../types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para adicionar token de autenticação
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('fins_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Interceptor para tratamento de erros
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('fins_token');
          localStorage.removeItem('fins_user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async register(userData: UserCreate): Promise<User> {
    const response: AxiosResponse<User> = await this.api.post('/auth/register', userData);
    return response.data;
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response: AxiosResponse<LoginResponse> = await this.api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response: AxiosResponse<User> = await this.api.get('/auth/me');
    return response.data;
  }

  async updateUser(userData: UserUpdate): Promise<User> {
    const response: AxiosResponse<User> = await this.api.put('/auth/me', userData);
    return response.data;
  }

  async deleteUser(): Promise<void> {
    await this.api.delete('/auth/me');
  }

  // Financial Profile endpoints
  async createFinancialProfile(profileData: FinancialProfileCreate): Promise<FinancialProfile> {
    const response: AxiosResponse<FinancialProfile> = await this.api.post('/financial/profile', profileData);
    return response.data;
  }

  async getFinancialProfile(): Promise<FinancialProfile> {
    const response: AxiosResponse<FinancialProfile> = await this.api.get('/financial/profile');
    return response.data;
  }

  async updateFinancialProfile(profileData: FinancialProfileUpdate): Promise<FinancialProfile> {
    const response: AxiosResponse<FinancialProfile> = await this.api.put('/financial/profile', profileData);
    return response.data;
  }

  // Expense endpoints
  async createExpense(expenseData: ExpenseCreate): Promise<Expense> {
    const response: AxiosResponse<Expense> = await this.api.post('/financial/expenses', expenseData);
    return response.data;
  }

  async getExpenses(skip = 0, limit = 100): Promise<Expense[]> {
    const response: AxiosResponse<Expense[]> = await this.api.get(`/financial/expenses?skip=${skip}&limit=${limit}`);
    return response.data;
  }

  async updateExpense(expenseId: string, expenseData: ExpenseUpdate): Promise<Expense> {
    const response: AxiosResponse<Expense> = await this.api.put(`/financial/expenses/${expenseId}`, expenseData);
    return response.data;
  }

  async deleteExpense(expenseId: string): Promise<void> {
    await this.api.delete(`/financial/expenses/${expenseId}`);
  }

  // Receipt endpoints
  async createReceipt(receiptData: ReceiptCreate): Promise<Receipt> {
    const response: AxiosResponse<Receipt> = await this.api.post('/financial/receipts', receiptData);
    return response.data;
  }

  async getReceipts(skip = 0, limit = 100): Promise<Receipt[]> {
    const response: AxiosResponse<Receipt[]> = await this.api.get(`/financial/receipts?skip=${skip}&limit=${limit}`);
    return response.data;
  }

  // Financial Summary endpoint
  async getFinancialSummary(): Promise<FinancialSummary> {
    const response: AxiosResponse<FinancialSummary> = await this.api.get('/financial/summary');
    return response.data;
  }

  // AI endpoints
  async getBalancePrediction(monthsAhead = 3): Promise<BalancePrediction> {
    const response: AxiosResponse<BalancePrediction> = await this.api.get(`/ai/predict/balance?months_ahead=${monthsAhead}`);
    return response.data;
  }

  async getSavingsPrediction(): Promise<SavingsPrediction> {
    const response: AxiosResponse<SavingsPrediction> = await this.api.get('/ai/predict/savings');
    return response.data;
  }

  async getRiskAnalysis(): Promise<RiskAnalysis> {
    const response: AxiosResponse<RiskAnalysis> = await this.api.get('/ai/analyze/risk');
    return response.data;
  }

  async getExpenseAnalysis(): Promise<ExpenseAnalysis> {
    const response: AxiosResponse<ExpenseAnalysis> = await this.api.get('/ai/analyze/expenses');
    return response.data;
  }

  async getFinancialInsights(): Promise<FinancialInsights> {
    const response: AxiosResponse<FinancialInsights> = await this.api.get('/ai/insights');
    return response.data;
  }

  async getAIHealthCheck(): Promise<any> {
    const response: AxiosResponse = await this.api.get('/ai/health');
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<any> {
    const response: AxiosResponse = await this.api.get('/health');
    return response.data;
  }
}

export const apiService = new ApiService();
export default apiService; 