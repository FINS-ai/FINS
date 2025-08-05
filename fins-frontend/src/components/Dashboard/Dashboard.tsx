import {
    AlertTriangle,
    BarChart3,
    Calendar,
    DollarSign,
    PiggyBank,
    TrendingDown,
    TrendingUp,
    Wallet
} from 'lucide-react';
import React from 'react';
import { useQuery } from 'react-query';
import { apiService } from '../../services/api';
import { FinancialSummary } from '../../types';
import { formatCurrency } from '../../utils/formatters';

const Dashboard: React.FC = () => {
  const { data: summary, isLoading, error } = useQuery<FinancialSummary>(
    'financialSummary',
    () => apiService.getFinancialSummary(),
    {
      refetchInterval: 30000, // Refetch every 30 seconds
    }
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <AlertTriangle className="mx-auto h-12 w-12 text-danger-500" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">Erro ao carregar dados</h3>
        <p className="mt-1 text-sm text-gray-500">
          Não foi possível carregar o resumo financeiro.
        </p>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="text-center py-8">
        <Wallet className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhum dado financeiro</h3>
        <p className="mt-1 text-sm text-gray-500">
          Configure seu perfil financeiro para começar.
        </p>
      </div>
    );
  }

  const totalExpenses = Object.values(summary.monthly_expenses).reduce((a, b) => a + b, 0);
  const savings = summary.monthly_salary - totalExpenses;
  const savingsRate = summary.monthly_salary > 0 ? (savings / summary.monthly_salary) * 100 : 0;

  const stats = [
    {
      name: 'Saldo Atual',
      value: formatCurrency(summary.current_balance),
      change: summary.net_flow_30_days,
      changeType: summary.net_flow_30_days >= 0 ? 'positive' : 'negative',
      icon: Wallet,
      color: 'bg-blue-500',
    },
    {
      name: 'Salário Mensal',
      value: formatCurrency(summary.monthly_salary),
      change: 0,
      changeType: 'neutral' as const,
      icon: DollarSign,
      color: 'bg-green-500',
    },
    {
      name: 'Despesas Mensais',
      value: formatCurrency(totalExpenses),
      change: 0,
      changeType: 'neutral' as const,
      icon: TrendingDown,
      color: 'bg-red-500',
    },
    {
      name: 'Poupança Mensal',
      value: formatCurrency(savings),
      change: savingsRate,
      changeType: savings >= 0 ? 'positive' : 'negative',
      icon: PiggyBank,
      color: 'bg-purple-500',
    },
  ];

  const recentExpenses = summary.last_30_days_expenses.slice(0, 5);
  const recentReceipts = summary.last_30_days_receipts.slice(0, 5);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Visão geral das suas finanças</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center">
                <div className={`p-2 rounded-lg ${stat.color}`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <div className="ml-4 flex-1">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
              {stat.change !== 0 && (
                <div className="mt-2 flex items-center">
                  {stat.changeType === 'positive' ? (
                    <TrendingUp className="h-4 w-4 text-success-500" />
                  ) : stat.changeType === 'negative' ? (
                    <TrendingDown className="h-4 w-4 text-danger-500" />
                  ) : null}
                  <span
                    className={`ml-1 text-sm font-medium ${
                      stat.changeType === 'positive'
                        ? 'text-success-600'
                        : stat.changeType === 'negative'
                        ? 'text-danger-600'
                        : 'text-gray-600'
                    }`}
                  >
                    {stat.changeType === 'positive' ? '+' : ''}
                    {typeof stat.change === 'number' && stat.change !== 0
                      ? stat.change > 100
                        ? `${stat.change.toFixed(1)}%`
                        : formatCurrency(stat.change)
                      : ''}
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Expenses */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Despesas Recentes</h3>
            <BarChart3 className="h-5 w-5 text-gray-400" />
          </div>
          <div className="space-y-3">
            {recentExpenses.length > 0 ? (
              recentExpenses.map((expense) => (
                <div key={expense.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{expense.description}</p>
                      <p className="text-xs text-gray-500">{expense.category}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">
                      -{formatCurrency(expense.amount)}
                    </p>
                    <p className="text-xs text-gray-500">
                      {new Date(expense.date).toLocaleDateString('pt-BR')}
                    </p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-gray-500 text-center py-4">
                Nenhuma despesa registrada nos últimos 30 dias
              </p>
            )}
          </div>
        </div>

        {/* Recent Receipts */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Recebimentos Recentes</h3>
            <Calendar className="h-5 w-5 text-gray-400" />
          </div>
          <div className="space-y-3">
            {recentReceipts.length > 0 ? (
              recentReceipts.map((receipt) => (
                <div key={receipt.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{receipt.description}</p>
                      <p className="text-xs text-gray-500">{receipt.category || 'Recebimento'}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">
                      +{formatCurrency(receipt.amount)}
                    </p>
                    <p className="text-xs text-gray-500">
                      {new Date(receipt.date).toLocaleDateString('pt-BR')}
                    </p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-gray-500 text-center py-4">
                Nenhum recebimento registrado nos últimos 30 dias
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Ações Rápidas</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="flex flex-col items-center p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors">
            <TrendingUp className="h-6 w-6 text-primary-600 mb-2" />
            <span className="text-sm font-medium text-primary-600">Nova Despesa</span>
          </button>
          <button className="flex flex-col items-center p-4 bg-success-50 rounded-lg hover:bg-success-100 transition-colors">
            <DollarSign className="h-6 w-6 text-success-600 mb-2" />
            <span className="text-sm font-medium text-success-600">Novo Recebimento</span>
          </button>
          <button className="flex flex-col items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
            <BarChart3 className="h-6 w-6 text-purple-600 mb-2" />
            <span className="text-sm font-medium text-purple-600">Ver Relatórios</span>
          </button>
          <button className="flex flex-col items-center p-4 bg-orange-50 rounded-lg hover:bg-orange-100 transition-colors">
            <PiggyBank className="h-6 w-6 text-orange-600 mb-2" />
            <span className="text-sm font-medium text-orange-600">IA Insights</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 