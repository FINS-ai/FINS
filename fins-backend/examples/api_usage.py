#!/usr/bin/env python3
"""
Exemplo de uso da API FINS
Este script demonstra como usar todos os endpoints principais da API
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any

class FINSAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def register_user(self, email: str, full_name: str, password: str) -> Dict[str, Any]:
        """Registra um novo usuário"""
        data = {
            "email": email,
            "full_name": full_name,
            "password": password
        }
        response = self.session.post(f"{self.base_url}/api/v1/auth/register", json=data)
        return response.json()
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Faz login do usuário"""
        data = {
            "username": email,
            "password": password
        }
        response = self.session.post(f"{self.base_url}/api/v1/auth/login", data=data)
        result = response.json()
        if "access_token" in result:
            self.auth_token = result["access_token"]
        return result
    
    def create_financial_profile(self, salary: float, current_balance: float, monthly_expenses: Dict[str, float]) -> Dict[str, Any]:
        """Cria um perfil financeiro"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        data = {
            "salary": salary,
            "current_balance": current_balance,
            "monthly_expenses": monthly_expenses
        }
        response = self.session.post(f"{self.base_url}/api/v1/financial/profile", json=data, headers=headers)
        return response.json()
    
    def add_expense(self, amount: float, category: str, description: str, date: str = None) -> Dict[str, Any]:
        """Adiciona uma despesa"""
        if date is None:
            date = datetime.now().isoformat()
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        data = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
        }
        response = self.session.post(f"{self.base_url}/api/v1/financial/expenses", json=data, headers=headers)
        return response.json()
    
    def add_receipt(self, amount: float, description: str, category: str = None, date: str = None) -> Dict[str, Any]:
        """Adiciona um recibo"""
        if date is None:
            date = datetime.now().isoformat()
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        data = {
            "amount": amount,
            "description": description,
            "date": date
        }
        if category:
            data["category"] = category
        
        response = self.session.post(f"{self.base_url}/api/v1/financial/receipts", json=data, headers=headers)
        return response.json()
    
    def get_financial_summary(self) -> Dict[str, Any]:
        """Obtém resumo financeiro"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(f"{self.base_url}/api/v1/financial/summary", headers=headers)
        return response.json()
    
    def get_balance_prediction(self, months_ahead: int = 3) -> Dict[str, Any]:
        """Obtém previsão de saldo"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(f"{self.base_url}/api/v1/ai/predict/balance?months_ahead={months_ahead}", headers=headers)
        return response.json()
    
    def get_savings_prediction(self) -> Dict[str, Any]:
        """Obtém previsão de poupança"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(f"{self.base_url}/api/v1/ai/predict/savings", headers=headers)
        return response.json()
    
    def get_risk_analysis(self) -> Dict[str, Any]:
        """Obtém análise de risco"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(f"{self.base_url}/api/v1/ai/analyze/risk", headers=headers)
        return response.json()
    
    def get_expense_analysis(self) -> Dict[str, Any]:
        """Obtém análise de despesas"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(f"{self.base_url}/api/v1/ai/analyze/expenses", headers=headers)
        return response.json()
    
    def get_complete_insights(self) -> Dict[str, Any]:
        """Obtém insights completos"""
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(f"{self.base_url}/api/v1/ai/insights", headers=headers)
        return response.json()

def main():
    """Exemplo completo de uso da API"""
    print("🚀 Exemplo de uso da API FINS")
    print("=" * 50)
    
    # Inicializar cliente
    client = FINSAPIClient()
    
    # 1. Registrar usuário
    print("\n1. Registrando usuário...")
    try:
        user_data = client.register_user(
            email="usuario.exemplo@fins.com",
            full_name="João Silva",
            password="senha123456"
        )
        print(f"✅ Usuário registrado: {user_data['email']}")
    except Exception as e:
        print(f"❌ Erro no registro: {e}")
        return
    
    # 2. Fazer login
    print("\n2. Fazendo login...")
    try:
        login_data = client.login("usuario.exemplo@fins.com", "senha123456")
        print(f"✅ Login realizado com sucesso")
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return
    
    # 3. Criar perfil financeiro
    print("\n3. Criando perfil financeiro...")
    try:
        profile_data = client.create_financial_profile(
            salary=5000.00,
            current_balance=10000.00,
            monthly_expenses={
                "alimentacao": 800.00,
                "transporte": 400.00,
                "saude": 300.00,
                "aluguel": 1500.00,
                "diversas": 500.00
            }
        )
        print(f"✅ Perfil financeiro criado - Salário: R$ {profile_data['salary']}")
    except Exception as e:
        print(f"❌ Erro ao criar perfil: {e}")
        return
    
    # 4. Adicionar algumas despesas
    print("\n4. Adicionando despesas...")
    expenses = [
        {"amount": 150.00, "category": "alimentacao", "description": "Almoço no restaurante"},
        {"amount": 80.00, "category": "transporte", "description": "Combustível"},
        {"amount": 200.00, "category": "saude", "description": "Consulta médica"},
        {"amount": 120.00, "category": "alimentacao", "description": "Supermercado"},
        {"amount": 300.00, "category": "diversas", "description": "Presente de aniversário"}
    ]
    
    for expense in expenses:
        try:
            result = client.add_expense(**expense)
            print(f"✅ Despesa adicionada: {expense['description']} - R$ {expense['amount']}")
        except Exception as e:
            print(f"❌ Erro ao adicionar despesa: {e}")
    
    # 5. Adicionar alguns recibos
    print("\n5. Adicionando recibos...")
    receipts = [
        {"amount": 5000.00, "description": "Salário", "category": "salario"},
        {"amount": 500.00, "description": "Freelance", "category": "renda_extra"},
        {"amount": 200.00, "description": "Reembolso", "category": "reembolso"}
    ]
    
    for receipt in receipts:
        try:
            result = client.add_receipt(**receipt)
            print(f"✅ Recibo adicionado: {receipt['description']} - R$ {receipt['amount']}")
        except Exception as e:
            print(f"❌ Erro ao adicionar recibo: {e}")
    
    # 6. Obter resumo financeiro
    print("\n6. Obtendo resumo financeiro...")
    try:
        summary = client.get_financial_summary()
        print(f"✅ Resumo obtido:")
        print(f"   - Saldo atual: R$ {summary['current_balance']}")
        print(f"   - Salário mensal: R$ {summary['monthly_salary']}")
        print(f"   - Despesas últimos 30 dias: R$ {summary['last_30_days_expenses']}")
        print(f"   - Recebimentos últimos 30 dias: R$ {summary['last_30_days_receipts']}")
        print(f"   - Fluxo líquido: R$ {summary['net_flow_30_days']}")
    except Exception as e:
        print(f"❌ Erro ao obter resumo: {e}")
    
    # 7. Análises de IA
    print("\n7. Executando análises de IA...")
    
    # Previsão de saldo
    try:
        balance_pred = client.get_balance_prediction(months_ahead=3)
        print(f"✅ Previsão de saldo (3 meses): R$ {balance_pred['predicted_balance']:.2f}")
        print(f"   - Acurácia do modelo: {balance_pred['model_accuracy']:.2%}")
    except Exception as e:
        print(f"❌ Erro na previsão de saldo: {e}")
    
    # Previsão de poupança
    try:
        savings_pred = client.get_savings_prediction()
        print(f"✅ Previsão de poupança:")
        print(f"   - Potencial mensal: R$ {savings_pred['monthly_savings_potential']:.2f}")
        print(f"   - Taxa de poupança: {savings_pred['savings_rate']:.2%}")
    except Exception as e:
        print(f"❌ Erro na previsão de poupança: {e}")
    
    # Análise de risco
    try:
        risk_analysis = client.get_risk_analysis()
        print(f"✅ Análise de risco:")
        print(f"   - Nível: {risk_analysis['risk_level']}")
        print(f"   - Pontuação: {risk_analysis['risk_score']:.1f}/100")
        print(f"   - Probabilidade de inadimplência: {risk_analysis['default_probability']:.2%}")
    except Exception as e:
        print(f"❌ Erro na análise de risco: {e}")
    
    # Análise de despesas
    try:
        expense_analysis = client.get_expense_analysis()
        print(f"✅ Análise de despesas:")
        print(f"   - Total mensal: R$ {expense_analysis['total_monthly_expenses']:.2f}")
        print(f"   - Tendência: {expense_analysis['expense_trend']}")
    except Exception as e:
        print(f"❌ Erro na análise de despesas: {e}")
    
    # 8. Insights completos
    print("\n8. Obtendo insights completos...")
    try:
        insights = client.get_complete_insights()
        print(f"✅ Insights obtidos:")
        print(f"   - Pontuação geral: {insights['overall_score']:.1f}/100")
        print(f"   - Insights principais: {len(insights['key_insights'])} encontrados")
        print(f"   - Ações recomendadas: {len(insights['action_items'])} itens")
        
        print("\n📋 Principais insights:")
        for insight in insights['key_insights'][:3]:  # Mostrar apenas os 3 primeiros
            print(f"   • {insight}")
        
        print("\n🎯 Ações recomendadas:")
        for action in insights['action_items'][:3]:  # Mostrar apenas as 3 primeiras
            print(f"   • {action}")
            
    except Exception as e:
        print(f"❌ Erro ao obter insights: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Exemplo concluído com sucesso!")
    print("📚 Acesse a documentação em: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 