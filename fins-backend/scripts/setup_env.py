#!/usr/bin/env python3
"""
Script para configurar o arquivo .env do FINS
"""

import os
import secrets
from pathlib import Path

def generate_secret_key():
    """Gera uma chave secreta segura para JWT"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Cria o arquivo .env com as configurações"""
    
    print("🚀 Configuração do Arquivo .env - FINS")
    print("=" * 50)
    
    # Verificar se já existe um arquivo .env
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        print("⚠️  Arquivo .env já existe!")
        response = input("Deseja sobrescrever? (s/N): ").lower()
        if response != 's':
            print("❌ Operação cancelada.")
            return
    
    print("\n📝 Por favor, forneça as informações do seu projeto Supabase:")
    print("(Você pode encontrar essas informações em: Supabase Dashboard > Settings > API)")
    
    # Coletar informações do usuário
    supabase_url = input("\n🔗 Project URL (ex: https://abc123.supabase.co): ").strip()
    supabase_key = input("🔑 Anon Public Key: ").strip()
    supabase_service_key = input("🔐 Service Role Secret Key: ").strip()
    
    # Gerar chave secreta
    secret_key = generate_secret_key()
    print(f"\n🔒 Chave secreta gerada automaticamente: {secret_key[:20]}...")
    
    # Construir DATABASE_URL
    if supabase_url:
        # Extrair project_ref da URL
        project_ref = supabase_url.split('//')[1].split('.')[0]
        database_url = f"postgresql://postgres:[YOUR-PASSWORD]@db.{project_ref}.supabase.co:5432/postgres"
    else:
        database_url = "postgresql://username:password@host:port/database"
    
    # Criar conteúdo do arquivo .env
    env_content = f"""# Supabase Configuration
SUPABASE_URL={supabase_url}
SUPABASE_KEY={supabase_key}
SUPABASE_SERVICE_KEY={supabase_service_key}

# JWT Configuration
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL={database_url}

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=FINS - Financial Intelligence System
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# ML Model Configuration
MODEL_PATH=./models/
"""
    
    # Salvar arquivo
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"\n✅ Arquivo .env criado com sucesso em: {env_path}")
        print("\n📋 Próximos passos:")
        print("1. ⚠️  IMPORTANTE: Configure a senha do banco no DATABASE_URL")
        print("2. 🧪 Teste a conexão: python scripts/execute_setup.py")
        print("3. 🚀 Execute o backend: python -m uvicorn app.main:app --reload")
        
        if "[YOUR-PASSWORD]" in database_url:
            print(f"\n⚠️  ATENÇÃO: Você precisa substituir [YOUR-PASSWORD] pela senha real do seu banco!")
            print("   Vá para: Supabase Dashboard > Settings > Database")
            print("   Copie a 'Connection string' e substitua a senha")
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo .env: {e}")

def main():
    """Função principal"""
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main() 