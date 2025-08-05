#!/bin/bash

# Script de inicialização para produção
# FINS - Financial Intelligence System

echo "🚀 Iniciando FINS Backend..."

# Verificar se as variáveis de ambiente necessárias estão definidas
if [ -z "$SUPABASE_URL" ]; then
    echo "❌ Erro: SUPABASE_URL não está definida"
    exit 1
fi

if [ -z "$SUPABASE_KEY" ]; then
    echo "❌ Erro: SUPABASE_KEY não está definida"
    exit 1
fi

if [ -z "$SECRET_KEY" ]; then
    echo "❌ Erro: SECRET_KEY não está definida"
    exit 1
fi

echo "✅ Variáveis de ambiente verificadas"

# Criar diretório de modelos se não existir
mkdir -p models

# Verificar se o banco de dados está acessível
echo "🔍 Verificando conexão com o banco de dados..."
python -c "
import os
import sys
sys.path.append('/app')
from app.database import db
try:
    client = db.get_client()
    print('✅ Conexão com Supabase estabelecida')
except Exception as e:
    print(f'❌ Erro ao conectar com Supabase: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Falha na verificação do banco de dados"
    exit 1
fi

# Definir porta (padrão: 8000)
PORT=${PORT:-8000}

echo "🌐 Iniciando servidor na porta $PORT"

# Iniciar a aplicação
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 1 \
    --log-level info 