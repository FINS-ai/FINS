# 🚀 Guia de Início Rápido - FINS Backend

Este guia te ajudará a configurar e executar o sistema FINS em menos de 10 minutos!

## 📋 Pré-requisitos

- Python 3.9 ou superior
- Conta no Supabase (gratuita)
- Git

## ⚡ Configuração Rápida

### 1. Clone e Configure
```bash
# Clone o repositório
git clone <seu-repositorio>
cd fins-backend

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
```

### 2. Configure o Supabase
1. Acesse [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Vá em Settings > API
4. Copie a URL e as chaves

### 3. Configure as Variáveis de Ambiente
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas credenciais
nano .env  # ou use seu editor preferido
```

Preencha as seguintes variáveis:
```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_anon_do_supabase
SUPABASE_SERVICE_KEY=sua_chave_service_do_supabase
SECRET_KEY=sua_chave_secreta_jwt
```

### 4. Configure o Banco de Dados
1. No Supabase, vá em SQL Editor
2. Execute o script: `scripts/setup_database.sql`

### 5. Execute a Aplicação
```bash
python -m app.main
```

🎉 **Pronto!** A API estará disponível em: http://localhost:8000

## 📚 Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Teste Rápido

Execute o script de testes:
```bash
python scripts/run_tests.py
```

Ou teste manualmente:
```bash
# Health check
curl http://localhost:8000/health

# Informações da API
curl http://localhost:8000/info
```

## 🔧 Comandos Úteis

```bash
# Executar com reload automático
uvicorn app.main:app --reload

# Executar em modo produção
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Executar testes
python scripts/run_tests.py

# Executar exemplo completo
python examples/api_usage.py

# Com Docker
docker-compose up -d
```

## 🚀 Deploy Rápido

### Render (Recomendado)
1. Conecte seu repositório ao Render
2. Configure as variáveis de ambiente
3. Deploy automático!

### Docker
```bash
docker build -t fins-backend .
docker run -p 8000:8000 fins-backend
```

## 📞 Suporte

- 📖 [Documentação Completa](README.md)
- 🐛 [Issues](https://github.com/seu-usuario/fins/issues)
- 💬 [Discord/Slack]

## 🎯 Próximos Passos

1. Explore a documentação da API
2. Teste os endpoints de IA
3. Configure um frontend
4. Personalize os modelos de ML

---

**Tempo estimado de configuração: 5-10 minutos** ⏱️ 