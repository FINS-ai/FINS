#!/usr/bin/env python3
"""
Script para executar testes básicos da API FINS
"""

import requests
import json
import time
from typing import Dict, Any

class FINSAPITester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def test_health_check(self) -> bool:
        """Testa o endpoint de health check"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ Health check: OK")
                return True
            else:
                print(f"❌ Health check: FAILED - Status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check: ERROR - {e}")
            return False
    
    def test_api_info(self) -> bool:
        """Testa o endpoint de informações da API"""
        try:
            response = self.session.get(f"{self.base_url}/info")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Info: OK - {data.get('name', 'Unknown')} v{data.get('version', 'Unknown')}")
                return True
            else:
                print(f"❌ API Info: FAILED - Status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API Info: ERROR - {e}")
            return False
    
    def test_user_registration(self, user_data: Dict[str, Any]) -> bool:
        """Testa o registro de usuário"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/auth/register",
                json=user_data
            )
            if response.status_code == 201:
                print("✅ User registration: OK")
                return True
            else:
                print(f"❌ User registration: FAILED - Status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ User registration: ERROR - {e}")
            return False
    
    def test_user_login(self, credentials: Dict[str, str]) -> bool:
        """Testa o login do usuário"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/auth/login",
                data=credentials
            )
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                print("✅ User login: OK")
                return True
            else:
                print(f"❌ User login: FAILED - Status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ User login: ERROR - {e}")
            return False
    
    def test_financial_profile_creation(self, profile_data: Dict[str, Any]) -> bool:
        """Testa a criação de perfil financeiro"""
        if not self.auth_token:
            print("❌ Financial profile creation: NO AUTH TOKEN")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.post(
                f"{self.base_url}/api/v1/financial/profile",
                json=profile_data,
                headers=headers
            )
            if response.status_code == 201:
                print("✅ Financial profile creation: OK")
                return True
            else:
                print(f"❌ Financial profile creation: FAILED - Status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Financial profile creation: ERROR - {e}")
            return False
    
    def test_expense_creation(self, expense_data: Dict[str, Any]) -> bool:
        """Testa a criação de despesa"""
        if not self.auth_token:
            print("❌ Expense creation: NO AUTH TOKEN")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.post(
                f"{self.base_url}/api/v1/financial/expenses",
                json=expense_data,
                headers=headers
            )
            if response.status_code == 201:
                print("✅ Expense creation: OK")
                return True
            else:
                print(f"❌ Expense creation: FAILED - Status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Expense creation: ERROR - {e}")
            return False
    
    def test_ai_health_check(self) -> bool:
        """Testa o health check dos modelos de IA"""
        if not self.auth_token:
            print("❌ AI health check: NO AUTH TOKEN")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.get(
                f"{self.base_url}/api/v1/ai/health",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ AI health check: OK - Status: {data.get('status', 'Unknown')}")
                return True
            else:
                print(f"❌ AI health check: FAILED - Status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ AI health check: ERROR - {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """Executa todos os testes"""
        print("🚀 Iniciando testes da API FINS...")
        print("=" * 50)
        
        # Dados de teste
        test_user = {
            "email": f"test_{int(time.time())}@example.com",
            "full_name": "Usuário Teste",
            "password": "testpassword123"
        }
        
        test_credentials = {
            "username": test_user["email"],
            "password": test_user["password"]
        }
        
        test_profile = {
            "salary": 5000.00,
            "current_balance": 10000.00,
            "monthly_expenses": {
                "alimentacao": 800.00,
                "transporte": 400.00,
                "saude": 300.00,
                "aluguel": 1500.00,
                "diversas": 500.00
            }
        }
        
        test_expense = {
            "amount": 150.00,
            "category": "alimentacao",
            "description": "Almoço no restaurante",
            "date": "2024-01-15T12:00:00Z"
        }
        
        # Executar testes
        tests = [
            ("Health Check", lambda: self.test_health_check()),
            ("API Info", lambda: self.test_api_info()),
            ("User Registration", lambda: self.test_user_registration(test_user)),
            ("User Login", lambda: self.test_user_login(test_credentials)),
            ("Financial Profile Creation", lambda: self.test_financial_profile_creation(test_profile)),
            ("Expense Creation", lambda: self.test_expense_creation(test_expense)),
            ("AI Health Check", lambda: self.test_ai_health_check()),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 Testando: {test_name}")
            if test_func():
                passed += 1
            time.sleep(1)  # Pequena pausa entre testes
        
        print("\n" + "=" * 50)
        print(f"📊 Resultados: {passed}/{total} testes passaram")
        
        if passed == total:
            print("🎉 Todos os testes passaram!")
            return True
        else:
            print("⚠️  Alguns testes falharam. Verifique os logs acima.")
            return False

def main():
    """Função principal"""
    import sys
    
    # Verificar se a API está rodando
    base_url = "http://localhost:8001"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"🔗 Conectando à API em: {base_url}")
    
    tester = FINSAPITester(base_url)
    
    # Testar se a API está acessível
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ API não está respondendo corretamente em {base_url}")
            print("   Certifique-se de que a API está rodando com: python -m app.main")
            return False
    except requests.exceptions.RequestException:
        print(f"❌ Não foi possível conectar à API em {base_url}")
        print("   Certifique-se de que a API está rodando com: python -m app.main")
        return False
    
    # Executar testes
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ Testes concluídos com sucesso!")
        return 0
    else:
        print("\n❌ Alguns testes falharam.")
        return 1

if __name__ == "__main__":
    exit(main()) 