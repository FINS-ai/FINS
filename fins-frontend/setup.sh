#!/bin/bash

echo "🚀 Configurando o Frontend FINS..."

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não está instalado. Por favor, instale o Node.js 16+ primeiro."
    exit 1
fi

# Verificar se o npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não está instalado. Por favor, instale o npm primeiro."
    exit 1
fi

echo "✅ Node.js e npm encontrados"

# Instalar dependências
echo "📦 Instalando dependências..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo "✅ Dependências instaladas com sucesso"

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "🔧 Criando arquivo .env..."
    cat > .env << EOF
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1

# Environment
REACT_APP_ENV=development

# Feature Flags
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_DEBUG=true
EOF
    echo "✅ Arquivo .env criado"
else
    echo "ℹ️  Arquivo .env já existe"
fi

echo ""
echo "🎉 Setup concluído com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Certifique-se de que o backend FINS está rodando na porta 8000"
echo "2. Execute 'npm start' para iniciar o servidor de desenvolvimento"
echo "3. Acesse http://localhost:3000 no seu navegador"
echo ""
echo "🔧 Scripts disponíveis:"
echo "  npm start    - Inicia o servidor de desenvolvimento"
echo "  npm build    - Gera build de produção"
echo "  npm test     - Executa os testes"
echo "" 