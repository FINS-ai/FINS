// User Types
export interface User {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  email: string;
  full_name: string;
  password: string;
  phone?: string;
}

export interface UserUpdate {
  full_name?: string;
  phone?: string;
}

// Auth Types
export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    full_name: string;
  };
}

// Financial Profile Types
export interface FinancialProfile {
  id: string;
  user_id: string;
  salary: number;
  current_balance: number;
  monthly_expenses: Record<string, number>;
  created_at: string;
  updated_at: string;
}

export interface FinancialProfileCreate {
  salary: number;
  current_balance: number;
  monthly_expenses: Record<string, number>;
}

export interface FinancialProfileUpdate {
  salary?: number;
  current_balance?: number;
  monthly_expenses?: Record<string, number>;
}

// Expense Types
export interface Expense {
  id: string;
  user_id: string;
  amount: number;
  category: string;
  description: string;
  date: string;
  created_at: string;
  updated_at: string;
}

export interface ExpenseCreate {
  amount: number;
  category: string;
  description: string;
  date: string;
}

export interface ExpenseUpdate {
  amount?: number;
  category?: string;
  description?: string;
  date?: string;
}

// Receipt Types
export interface Receipt {
  id: string;
  user_id: string;
  amount: number;
  description: string;
  date: string;
  category?: string;
  created_at: string;
  updated_at: string;
}

export interface ReceiptCreate {
  amount: number;
  description: string;
  date: string;
  category?: string;
}

export interface ReceiptUpdate {
  amount?: number;
  description?: string;
  date?: string;
  category?: string;
}

// Financial Summary Types
export interface FinancialSummary {
  current_balance: number;
  monthly_salary: number;
  monthly_expenses: Record<string, number>;
  total_monthly_expenses: number;
  last_30_days_expenses: Expense[];
  last_30_days_receipts: Receipt[];
  net_flow_30_days: number;
}

// AI Analysis Types
export interface BalancePrediction {
  predicted_balance: number;
  confidence_interval: {
    lower: number;
    upper: number;
  };
  prediction_date: string;
  model_accuracy: number;
}

export interface SavingsPrediction {
  monthly_savings_potential: number;
  yearly_savings_potential: number;
  savings_rate: number;
  recommendations: string[];
}

export interface RiskAnalysis {
  risk_level: 'baixo' | 'médio' | 'alto' | 'crítico';
  risk_score: number;
  default_probability: number;
  risk_factors: string[];
  recommendations: string[];
}

export interface ExpenseAnalysis {
  total_monthly_expenses: number;
  expenses_by_category: Record<string, number>;
  expense_trend: 'increasing' | 'decreasing' | 'stable';
  unusual_expenses: Expense[];
  budget_recommendations: string[];
}

export interface FinancialInsights {
  balance_prediction: BalancePrediction;
  savings_prediction: SavingsPrediction;
  risk_analysis: RiskAnalysis;
  expense_analysis: ExpenseAnalysis;
  overall_health_score: number;
  key_insights: string[];
  action_items: string[];
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

// Chart Data Types
export interface ChartData {
  name: string;
  value: number;
  color?: string;
}

export interface TimeSeriesData {
  date: string;
  value: number;
} 