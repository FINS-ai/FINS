#!/usr/bin/env python3
"""
Script para executar automaticamente o setup do banco de dados FINS
"""

import os
import sys
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Adicionar o diretório raiz ao path para importar configurações
sys.path.append(str(Path(__file__).parent.parent))

from app.config import settings

def execute_sql_script():
    """Executa o script SQL de setup do banco de dados"""
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar se as credenciais do Supabase estão configuradas
    if not settings.supabase_url or not settings.supabase_service_key:
        print("❌ Erro: SUPABASE_URL e SUPABASE_SERVICE_KEY devem estar configurados no .env")
        print("Por favor, configure suas credenciais do Supabase primeiro.")
        return False
    
    try:
        # Criar cliente Supabase com service key (tem permissões de admin)
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_key
        )
        
        print("🔗 Conectando ao Supabase...")
        
        # Ler o arquivo SQL
        sql_file_path = Path(__file__).parent / "setup_database.sql"
        
        if not sql_file_path.exists():
            print(f"❌ Erro: Arquivo {sql_file_path} não encontrado")
            return False
        
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        print("📝 Executando script de setup do banco de dados...")
        
        # Executar o SQL
        result = supabase.rpc('exec_sql', {'sql': sql_content})
        
        print("✅ Setup do banco de dados concluído com sucesso!")
        print("📊 Tabelas criadas:")
        print("   - users")
        print("   - financial_profiles") 
        print("   - expenses")
        print("   - receipts")
        print("🔒 Políticas de segurança RLS configuradas")
        print("📈 Índices de performance criados")
        print("🔄 Triggers para updated_at configurados")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar setup: {e}")
        print("\n💡 Alternativas:")
        print("1. Execute manualmente via Supabase Dashboard > SQL Editor")
        print("2. Use o Supabase CLI: supabase db reset")
        return False

def main():
    """Função principal"""
    print("🚀 FINS - Setup do Banco de Dados")
    print("=" * 40)
    
    # Verificar se o arquivo .env existe
    env_file = Path(__file__).parent.parent / ".env"
    if not env_file.exists():
        print("⚠️  Arquivo .env não encontrado")
        print("📝 Copie .env.example para .env e configure suas credenciais")
        return
    
    success = execute_sql_script()
    
    if success:
        print("\n🎉 Setup concluído! Você pode agora executar o backend:")
        print("   python -m uvicorn app.main:app --reload")
    else:
        print("\n❌ Setup falhou. Verifique as configurações e tente novamente.")

if __name__ == "__main__":
    main() 