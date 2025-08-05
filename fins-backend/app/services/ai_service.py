import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from supabase import Client
from app.models.ai_models import (
    BalancePrediction, SavingsPrediction, RiskAnalysis, 
    ExpenseAnalysis, FinancialInsights, RiskLevel
)
from app.models.user import ExpenseCategory
import logging
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, classification_report
import xgboost as xgb
from prophet import Prophet
import json
import pickle
import os

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, db: Client):
        self.db = db
        self.models_path = "./models/"
        self._ensure_models_directory()
        self.scaler = StandardScaler()
        
    def _ensure_models_directory(self):
        """Garante que o diretório de modelos existe"""
        if not os.path.exists(self.models_path):
            os.makedirs(self.models_path)
    
    async def get_user_financial_data(self, user_id: str, months: int = 12) -> pd.DataFrame:
        """Coleta dados financeiros do usuário para análise"""
        try:
            # Busca perfil financeiro
            profile_result = self.db.table("financial_profiles").select("*").eq("user_id", user_id).execute()
            if not profile_result.data:
                return pd.DataFrame()
            
            profile = profile_result.data[0]
            
            # Busca despesas dos últimos meses
            start_date = datetime.utcnow() - timedelta(days=months * 30)
            expenses_result = self.db.table("expenses").select("*").eq("user_id", user_id).gte("date", start_date.isoformat()).execute()
            
            # Busca recibos dos últimos meses
            receipts_result = self.db.table("receipts").select("*").eq("user_id", user_id).gte("date", start_date.isoformat()).execute()
            
            # Cria DataFrame com dados financeiros
            data = []
            
            # Adiciona dados de despesas
            for expense in expenses_result.data:
                data.append({
                    'date': expense['date'],
                    'amount': -expense['amount'],  # Negativo para despesas
                    'type': 'expense',
                    'category': expense['category'],
                    'description': expense['description']
                })
            
            # Adiciona dados de recibos
            for receipt in receipts_result.data:
                data.append({
                    'date': receipt['date'],
                    'amount': receipt['amount'],  # Positivo para recibos
                    'type': 'receipt',
                    'category': receipt.get('category', 'diversas'),
                    'description': receipt['description']
                })
            
            df = pd.DataFrame(data)
            if df.empty:
                return df
            
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Calcula saldo acumulado
            df['balance'] = profile['current_balance'] + df['amount'].cumsum()
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados financeiros: {e}")
            return pd.DataFrame()
    
    async def predict_balance(self, user_id: str, months_ahead: int = 3) -> BalancePrediction:
        """Previsão do saldo futuro usando Prophet"""
        try:
            df = await self.get_user_financial_data(user_id)
            if df.empty:
                raise ValueError("Dados insuficientes para previsão")
            
            # Prepara dados para Prophet
            prophet_df = df.groupby(df['date'].dt.date)['amount'].sum().reset_index()
            prophet_df.columns = ['ds', 'y']
            prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])
            
            # Treina modelo Prophet
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                changepoint_prior_scale=0.05
            )
            model.fit(prophet_df)
            
            # Faz previsão
            future_dates = model.make_future_dataframe(periods=months_ahead * 30)
            forecast = model.predict(future_dates)
            
            # Calcula intervalo de confiança
            last_forecast = forecast.iloc[-1]
            predicted_balance = last_forecast['yhat']
            lower_bound = last_forecast['yhat_lower']
            upper_bound = last_forecast['yhat_upper']
            
            # Calcula acurácia do modelo
            actual = prophet_df['y'].values
            predicted = forecast['yhat'][:len(actual)].values
            mae = mean_absolute_error(actual, predicted)
            accuracy = max(0, 1 - mae / abs(actual).mean()) if abs(actual).mean() > 0 else 0
            
            return BalancePrediction(
                predicted_balance=predicted_balance,
                confidence_interval_lower=lower_bound,
                confidence_interval_upper=upper_bound,
                prediction_date=datetime.utcnow(),
                model_accuracy=accuracy
            )
            
        except Exception as e:
            logger.error(f"Erro na previsão de saldo: {e}")
            raise
    
    async def predict_savings(self, user_id: str) -> SavingsPrediction:
        """Previsão da capacidade de poupança"""
        try:
            df = await self.get_user_financial_data(user_id)
            if df.empty:
                raise ValueError("Dados insuficientes para análise")
            
            # Calcula métricas de poupança
            monthly_data = df.groupby(df['date'].dt.to_period('M')).agg({
                'amount': 'sum'
            }).reset_index()
            
            # Calcula potencial de poupança baseado na média dos últimos meses
            avg_monthly_flow = monthly_data['amount'].mean()
            monthly_savings_potential = max(0, avg_monthly_flow * 0.2)  # 20% do fluxo médio
            annual_savings_potential = monthly_savings_potential * 12
            
            # Calcula taxa de poupança
            profile_result = self.db.table("financial_profiles").select("salary").eq("user_id", user_id).execute()
            if profile_result.data:
                salary = profile_result.data[0]['salary']
                savings_rate = monthly_savings_potential / salary if salary > 0 else 0
            else:
                savings_rate = 0
            
            # Gera recomendações
            recommendations = []
            if savings_rate < 0.1:
                recommendations.append("Considere reduzir despesas não essenciais")
                recommendations.append("Estabeleça um orçamento mensal")
            if avg_monthly_flow < 0:
                recommendations.append("Suas despesas estão superando suas receitas")
                recommendations.append("Analise suas despesas por categoria")
            
            return SavingsPrediction(
                monthly_savings_potential=monthly_savings_potential,
                annual_savings_potential=annual_savings_potential,
                savings_rate=savings_rate,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Erro na previsão de poupança: {e}")
            raise
    
    async def analyze_risk(self, user_id: str) -> RiskAnalysis:
        """Análise de risco de inadimplência"""
        try:
            df = await self.get_user_financial_data(user_id)
            if df.empty:
                raise ValueError("Dados insuficientes para análise de risco")
            
            # Calcula features de risco
            features = self._calculate_risk_features(df)
            
            # Calcula pontuação de risco
            risk_score = self._calculate_risk_score(features)
            
            # Determina nível de risco
            risk_level = self._determine_risk_level(risk_score)
            
            # Calcula probabilidade de inadimplência
            default_probability = risk_score / 100
            
            # Identifica fatores de risco
            risk_factors = self._identify_risk_factors(features)
            
            # Gera recomendações
            recommendations = self._generate_risk_recommendations(features, risk_level)
            
            return RiskAnalysis(
                risk_level=risk_level,
                risk_score=risk_score,
                default_probability=default_probability,
                risk_factors=risk_factors,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Erro na análise de risco: {e}")
            raise
    
    async def analyze_expenses(self, user_id: str) -> ExpenseAnalysis:
        """Análise detalhada de despesas"""
        try:
            df = await self.get_user_financial_data(user_id)
            if df.empty:
                raise ValueError("Dados insuficientes para análise de despesas")
            
            # Filtra apenas despesas
            expenses_df = df[df['amount'] < 0].copy()
            expenses_df['amount'] = abs(expenses_df['amount'])
            
            # Calcula total de despesas mensais
            monthly_expenses = expenses_df.groupby(expenses_df['date'].dt.to_period('M'))['amount'].sum()
            total_monthly_expenses = monthly_expenses.mean()
            
            # Despesas por categoria
            expenses_by_category = expenses_df.groupby('category')['amount'].sum().to_dict()
            
            # Determina tendência das despesas
            if len(monthly_expenses) >= 2:
                trend = monthly_expenses.iloc[-1] - monthly_expenses.iloc[-2]
                if trend > 0:
                    expense_trend = "crescendo"
                elif trend < 0:
                    expense_trend = "decrescendo"
                else:
                    expense_trend = "estável"
            else:
                expense_trend = "estável"
            
            # Detecta despesas incomuns
            unusual_expenses = self._detect_unusual_expenses(expenses_df)
            
            # Gera recomendações de orçamento
            budget_recommendations = self._generate_budget_recommendations(expenses_by_category, total_monthly_expenses)
            
            return ExpenseAnalysis(
                total_monthly_expenses=total_monthly_expenses,
                expenses_by_category=expenses_by_category,
                expense_trend=expense_trend,
                unusual_expenses=unusual_expenses,
                budget_recommendations=budget_recommendations
            )
            
        except Exception as e:
            logger.error(f"Erro na análise de despesas: {e}")
            raise
    
    async def generate_financial_insights(self, user_id: str) -> FinancialInsights:
        """Gera insights financeiros completos"""
        try:
            # Executa todas as análises
            balance_prediction = await self.predict_balance(user_id)
            savings_prediction = await self.predict_savings(user_id)
            risk_analysis = await self.analyze_risk(user_id)
            expense_analysis = await self.analyze_expenses(user_id)
            
            # Calcula pontuação geral
            overall_score = self._calculate_overall_score(
                balance_prediction, savings_prediction, risk_analysis, expense_analysis
            )
            
            # Gera insights principais
            key_insights = self._generate_key_insights(
                balance_prediction, savings_prediction, risk_analysis, expense_analysis
            )
            
            # Gera itens de ação
            action_items = self._generate_action_items(
                balance_prediction, savings_prediction, risk_analysis, expense_analysis
            )
            
            return FinancialInsights(
                user_id=user_id,
                balance_prediction=balance_prediction,
                savings_prediction=savings_prediction,
                risk_analysis=risk_analysis,
                expense_analysis=expense_analysis,
                overall_score=overall_score,
                key_insights=key_insights,
                action_items=action_items
            )
            
        except Exception as e:
            logger.error(f"Erro ao gerar insights financeiros: {e}")
            raise
    
    def _calculate_risk_features(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calcula features para análise de risco"""
        features = {}
        
        # Fluxo de caixa médio
        features['avg_cash_flow'] = df['amount'].mean()
        
        # Variabilidade do fluxo de caixa
        features['cash_flow_volatility'] = df['amount'].std()
        
        # Frequência de despesas negativas
        negative_months = (df.groupby(df['date'].dt.to_period('M'))['amount'].sum() < 0).sum()
        total_months = len(df.groupby(df['date'].dt.to_period('M')))
        features['negative_flow_frequency'] = negative_months / total_months if total_months > 0 else 0
        
        # Saldo mínimo
        features['min_balance'] = df['balance'].min()
        
        # Tendência do saldo
        if len(df) >= 2:
            features['balance_trend'] = (df['balance'].iloc[-1] - df['balance'].iloc[0]) / len(df)
        else:
            features['balance_trend'] = 0
        
        return features
    
    def _calculate_risk_score(self, features: Dict[str, float]) -> float:
        """Calcula pontuação de risco (0-100)"""
        score = 0
        
        # Fluxo de caixa negativo
        if features['avg_cash_flow'] < 0:
            score += 30
        
        # Alta volatilidade
        if features['cash_flow_volatility'] > abs(features['avg_cash_flow']) * 2:
            score += 20
        
        # Frequência de fluxo negativo
        score += features['negative_flow_frequency'] * 25
        
        # Saldo baixo
        if features['min_balance'] < 0:
            score += 25
        
        # Tendência negativa
        if features['balance_trend'] < 0:
            score += 10
        
        return min(100, score)
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """Determina nível de risco baseado na pontuação"""
        if risk_score < 25:
            return RiskLevel.BAIXO
        elif risk_score < 50:
            return RiskLevel.MEDIO
        elif risk_score < 75:
            return RiskLevel.ALTO
        else:
            return RiskLevel.CRITICO
    
    def _identify_risk_factors(self, features: Dict[str, float]) -> List[str]:
        """Identifica fatores de risco específicos"""
        factors = []
        
        if features['avg_cash_flow'] < 0:
            factors.append("Fluxo de caixa negativo")
        
        if features['cash_flow_volatility'] > abs(features['avg_cash_flow']) * 2:
            factors.append("Alta volatilidade financeira")
        
        if features['negative_flow_frequency'] > 0.5:
            factors.append("Frequentes meses com saldo negativo")
        
        if features['min_balance'] < 0:
            factors.append("Saldo negativo em alguns períodos")
        
        if features['balance_trend'] < 0:
            factors.append("Tendência de queda no saldo")
        
        return factors
    
    def _generate_risk_recommendations(self, features: Dict[str, float], risk_level: RiskLevel) -> List[str]:
        """Gera recomendações para reduzir risco"""
        recommendations = []
        
        if features['avg_cash_flow'] < 0:
            recommendations.append("Reduza despesas não essenciais")
            recommendations.append("Busque fontes adicionais de renda")
        
        if features['cash_flow_volatility'] > abs(features['avg_cash_flow']) * 2:
            recommendations.append("Estabilize seus gastos mensais")
            recommendations.append("Crie um fundo de emergência")
        
        if risk_level in [RiskLevel.ALTO, RiskLevel.CRITICO]:
            recommendations.append("Considere buscar orientação financeira")
            recommendations.append("Priorize o pagamento de dívidas")
        
        return recommendations
    
    def _detect_unusual_expenses(self, expenses_df: pd.DataFrame) -> List[Dict]:
        """Detecta despesas incomuns"""
        unusual = []
        
        # Despesas muito altas (acima de 2 desvios padrão)
        mean_amount = expenses_df['amount'].mean()
        std_amount = expenses_df['amount'].std()
        threshold = mean_amount + 2 * std_amount
        
        high_expenses = expenses_df[expenses_df['amount'] > threshold]
        for _, expense in high_expenses.iterrows():
            unusual.append({
                'date': expense['date'].strftime('%Y-%m-%d'),
                'amount': expense['amount'],
                'category': expense['category'],
                'description': expense['description'],
                'reason': 'Valor muito alto'
            })
        
        return unusual
    
    def _generate_budget_recommendations(self, expenses_by_category: Dict, total_monthly: float) -> List[str]:
        """Gera recomendações de orçamento"""
        recommendations = []
        
        # Identifica categorias com maior gasto
        if expenses_by_category:
            max_category = max(expenses_by_category.items(), key=lambda x: x[1])
            if max_category[1] > total_monthly * 0.4:  # Mais de 40% do total
                recommendations.append(f"Considere reduzir gastos em {max_category[0]}")
        
        recommendations.append("Estabeleça limites mensais por categoria")
        recommendations.append("Monitore seus gastos regularmente")
        
        return recommendations
    
    def _calculate_overall_score(self, balance_pred: BalancePrediction, 
                               savings_pred: SavingsPrediction, 
                               risk_analysis: RiskAnalysis, 
                               expense_analysis: ExpenseAnalysis) -> float:
        """Calcula pontuação geral de saúde financeira"""
        score = 0
        
        # Pontuação baseada no risco (inversa)
        score += (100 - risk_analysis.risk_score) * 0.4
        
        # Pontuação baseada na capacidade de poupança
        score += min(100, savings_pred.savings_rate * 100) * 0.3
        
        # Pontuação baseada na tendência de despesas
        if expense_analysis.expense_trend == "decrescendo":
            score += 20
        elif expense_analysis.expense_trend == "estável":
            score += 10
        
        # Pontuação baseada na acurácia do modelo de previsão
        score += balance_pred.model_accuracy * 10
        
        return min(100, score)
    
    def _generate_key_insights(self, balance_pred: BalancePrediction, 
                             savings_pred: SavingsPrediction, 
                             risk_analysis: RiskAnalysis, 
                             expense_analysis: ExpenseAnalysis) -> List[str]:
        """Gera insights principais"""
        insights = []
        
        if risk_analysis.risk_level in [RiskLevel.ALTO, RiskLevel.CRITICO]:
            insights.append("Seu perfil financeiro apresenta riscos significativos")
        
        if savings_pred.savings_rate < 0.1:
            insights.append("Sua capacidade de poupança está abaixo do recomendado")
        
        if expense_analysis.expense_trend == "crescendo":
            insights.append("Suas despesas estão aumentando")
        
        if balance_pred.predicted_balance < 0:
            insights.append("Projeção indica saldo negativo nos próximos meses")
        
        return insights
    
    def _generate_action_items(self, balance_pred: BalancePrediction, 
                             savings_pred: SavingsPrediction, 
                             risk_analysis: RiskAnalysis, 
                             expense_analysis: ExpenseAnalysis) -> List[str]:
        """Gera itens de ação recomendados"""
        actions = []
        
        actions.extend(risk_analysis.recommendations[:2])  # Top 2 recomendações de risco
        actions.extend(savings_pred.recommendations[:2])   # Top 2 recomendações de poupança
        actions.extend(expense_analysis.budget_recommendations[:2])  # Top 2 recomendações de orçamento
        
        return list(set(actions))  # Remove duplicatas 