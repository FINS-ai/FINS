# FINS - Financial Intelligence System

Sistema de Inteligência Artificial para Auxílio Financeiro Pessoal

## 📋 Descrição

O FINS é uma plataforma completa de análise financeira pessoal que utiliza inteligência artificial para fornecer insights, previsões e recomendações financeiras personalizadas. O sistema oferece análise de risco, previsão de saldo, capacidade de poupança e muito mais.

## 🚀 Funcionalidades

### 👤 Gestão de Usuários
- Cadastro e autenticação segura com JWT
- Perfis de usuário personalizáveis
- Sistema de permissões

### 💰 Gestão Financeira
- Cadastro de dados financeiros (salário, saldo, despesas)
- Categorização de despesas
- Registro de despesas e recibos
- Atualização automática de saldo em tempo real
- Resumos financeiros detalhados

### 🤖 Inteligência Artificial
- **Previsão de Saldo**: Análise temporal com Prophet
- **Análise de Risco**: Avaliação de inadimplência
- **Previsão de Poupança**: Capacidade de economizar
- **Análise de Despesas**: Detecção de padrões e anomalias
- **Insights Personalizados**: Recomendações baseadas em IA

### 📊 Pipeline de Dados
- Limpeza automática de dados
- Normalização de categorias
- Engenharia de atributos
- Detecção de sazonalidade e tendências

## 🛠️ Tecnologias

### Backend
- **FastAPI**: Framework web moderno e rápido
- **Python 3.9+**: Linguagem principal
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI

### Banco de Dados
- **Supabase**: Backend-as-a-Service com PostgreSQL
- **SQLAlchemy**: ORM (opcional para migrações)

### IA/ML
- **Prophet**: Previsão temporal
- **Scikit-Learn**: Algoritmos de ML
- **XGBoost**: Modelos de boosting
- **Pandas & NumPy**: Manipulação de dados

### Autenticação
- **JWT**: Tokens de autenticação
- **Passlib**: Hash de senhas
- **Python-Jose**: Manipulação de JWT

## 📦 Instalação

### Pré-requisitos
- Python 3.9 ou superior
- Conta no Supabase
- Git

### 1. Clone o repositório
```bash
git clone <repository-url>
cd fins-backend
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Copie o arquivo de exemplo e configure suas credenciais:
```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
# Supabase Configuration
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_anon_do_supabase
SUPABASE_SERVICE_KEY=sua_chave_service_do_supabase

# JWT Configuration
SECRET_KEY=sua_chave_secreta_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sua_url_do_banco

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=FINS - Financial Intelligence System
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# ML Model Configuration
MODEL_PATH=./models/
```

### 5. Configure o Supabase
Crie as seguintes tabelas no seu projeto Supabase:

#### Tabela: users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    phone VARCHAR,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Tabela: financial_profiles
```sql
CREATE TABLE financial_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    salary DECIMAL(10,2) NOT NULL,
    current_balance DECIMAL(10,2) NOT NULL,
    monthly_expenses JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);
```

#### Tabela: expenses
```sql
CREATE TABLE expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Tabela: receipts
```sql
CREATE TABLE receipts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    category VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 6. Execute a aplicação
```bash
python -m app.main
```

A API estará disponível em: http://localhost:8000

## 📚 Documentação da API

### Swagger UI
Acesse a documentação interativa em: http://localhost:8000/docs

### ReDoc
Documentação alternativa em: http://localhost:8000/redoc

## 🔌 Endpoints Principais

### Autenticação
- `POST /api/v1/auth/register` - Registro de usuário
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Informações do usuário atual
- `PUT /api/v1/auth/me` - Atualizar perfil
- `DELETE /api/v1/auth/me` - Deletar conta

### Gestão Financeira
- `POST /api/v1/financial/profile` - Criar perfil financeiro
- `GET /api/v1/financial/profile` - Obter perfil financeiro
- `PUT /api/v1/financial/profile` - Atualizar perfil financeiro
- `POST /api/v1/financial/expenses` - Criar despesa
- `GET /api/v1/financial/expenses` - Listar despesas
- `POST /api/v1/financial/receipts` - Criar recibo
- `GET /api/v1/financial/receipts` - Listar recibos
- `GET /api/v1/financial/summary` - Resumo financeiro

### Inteligência Artificial
- `GET /api/v1/ai/predict/balance` - Previsão de saldo
- `GET /api/v1/ai/predict/savings` - Previsão de poupança
- `GET /api/v1/ai/analyze/risk` - Análise de risco
- `GET /api/v1/ai/analyze/expenses` - Análise de despesas
- `GET /api/v1/ai/insights` - Insights completos
- `GET /api/v1/ai/health` - Status dos modelos

## 🔐 Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação. Para acessar endpoints protegidos:

1. Faça login em `/api/v1/auth/login`
2. Use o token retornado no header: `Authorization: Bearer <token>`

## 📊 Modelos de IA

### Prophet (Previsão Temporal)
- Análise de sazonalidade
- Detecção de tendências
- Intervalos de confiança

### Análise de Risco
- Pontuação de risco (0-100)
- Fatores de risco identificados
- Recomendações personalizadas

### Análise de Despesas
- Categorização automática
- Detecção de anomalias
- Padrões de gastos

## 🚀 Deploy

### Render
1. Conecte seu repositório ao Render
2. Configure as variáveis de ambiente
3. Deploy automático

### Docker (Opcional)
```bash
docker build -t fins-backend .
docker run -p 8000:8000 fins-backend
```

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar testes
pytest
```

## 📈 Monitoramento

- Logs estruturados
- Métricas de performance
- Health checks
- Status dos modelos de IA

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Entre em contato: [seu-email@exemplo.com]

## 🔄 Roadmap

- [ ] Interface web (Frontend)
- [ ] Notificações push
- [ ] Integração com bancos
- [ ] Relatórios avançados
- [ ] API para terceiros
- [ ] Mobile app 