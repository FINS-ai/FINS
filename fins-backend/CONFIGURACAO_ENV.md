# Configuração das Variáveis de Ambiente - FINS

## Passo 1: Obter Credenciais do Supabase

### 1.1 Acesse o Supabase Dashboard
1. Vá para [supabase.com](https://supabase.com)
2. Faça login na sua conta
3. Selecione seu projeto FINS

### 1.2 Obter as Credenciais
1. No menu lateral, clique em **"Settings"** (ícone de engrenagem)
2. Clique em **"API"**
3. Você verá duas seções importantes:

#### **Project URL**
- Copie o valor de **"Project URL"**
- Exemplo: `https://abcdefghijklmnop.supabase.co`

#### **Project API keys**
- **anon public**: Esta é sua `SUPABASE_KEY`
- **service_role secret**: Esta é sua `SUPABASE_SERVICE_KEY`

⚠️ **IMPORTANTE**: A `service_role` tem permissões de admin, mantenha-a segura!

## Passo 2: Criar o Arquivo .env

### 2.1 Copiar o Template
```bash
cd fins-backend
copy env.example .env
```

### 2.2 Editar o Arquivo .env
Abra o arquivo `.env` e substitua os valores:

```env
# Supabase Configuration
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-anon-key-aqui
SUPABASE_SERVICE_KEY=sua-service-key-aqui

# JWT Configuration
SECRET_KEY=uma-chave-secreta-muito-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=postgresql://postgres:[SEU-PASSWORD]@db.[SEU-PROJECT-REF].supabase.co:5432/postgres

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=FINS - Financial Intelligence System
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# ML Model Configuration
MODEL_PATH=./models/
```

## Passo 3: Configurar Cada Variável

### 3.1 Supabase Configuration

#### SUPABASE_URL
- Use o **Project URL** do Supabase
- Formato: `https://[project-ref].supabase.co`

#### SUPABASE_KEY
- Use a **anon public** key
- Formato: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

#### SUPABASE_SERVICE_KEY
- Use a **service_role secret** key
- Formato: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### 3.2 JWT Configuration

#### SECRET_KEY
- Gere uma chave secreta segura
- Você pode usar este comando para gerar:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### ALGORITHM
- Mantenha como `HS256`

#### ACCESS_TOKEN_EXPIRE_MINUTES
- Mantenha como `30` (ou ajuste conforme necessário)

### 3.3 Database Configuration

#### DATABASE_URL
- No Supabase Dashboard → Settings → Database
- Copie a **Connection string** da seção "Connection string"
- Substitua `[YOUR-PASSWORD]` pela senha do seu banco

### 3.4 API Configuration

#### API_V1_STR
- Mantenha como `/api/v1`

#### PROJECT_NAME
- Mantenha como `FINS - Financial Intelligence System`

#### BACKEND_CORS_ORIGINS
- Mantenha como está para desenvolvimento local
- Para produção, adicione seu domínio

### 3.5 ML Model Configuration

#### MODEL_PATH
- Mantenha como `./models/`

## Passo 4: Verificar a Configuração

### 4.1 Testar a Conexão
```bash
cd fins-backend
python scripts/execute_setup.py
```

Se tudo estiver correto, você verá:
```
✅ Setup do banco de dados concluído com sucesso!
```

### 4.2 Executar o Backend
```bash
python -m uvicorn app.main:app --reload
```

Acesse: `http://localhost:8000/docs`

## Exemplo Completo de .env

```env
# Supabase Configuration
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzNzQ5NjAwMCwiZXhwIjoxOTUzMDcyMDAwfQ.example
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjM3NDk2MDAwLCJleHAiOjE5NTMwNzIwMDB9.example

# JWT Configuration
SECRET_KEY=minha-chave-secreta-muito-segura-123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=postgresql://postgres:minhasenha123@db.abcdefghijklmnop.supabase.co:5432/postgres

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=FINS - Financial Intelligence System
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# ML Model Configuration
MODEL_PATH=./models/
```

## Troubleshooting

### Erro: "SUPABASE_URL not found"
- Verifique se o arquivo `.env` está na pasta `fins-backend/`
- Verifique se não há espaços extras nas variáveis

### Erro: "Invalid API key"
- Verifique se copiou a chave correta (anon vs service_role)
- Verifique se não há caracteres extras

### Erro: "Connection failed"
- Verifique se o `DATABASE_URL` está correto
- Verifique se a senha do banco está correta

### Erro: "Permission denied"
- Use a **service_role** key para operações de admin
- Use a **anon** key para operações normais

## Próximos Passos

Após configurar o `.env`:
1. ✅ Execute o setup do banco: `python scripts/execute_setup.py`
2. ✅ Execute o backend: `python -m uvicorn app.main:app --reload`
3. ✅ Teste a API: `http://localhost:8000/docs`
4. ✅ Execute os testes: `python scripts/run_tests.py` 