# Setup Manual do Banco de Dados FINS

## Método 1: Via Supabase Dashboard (Recomendado)

### Passo 1: Acesse o Supabase Dashboard
1. Vá para [supabase.com](https://supabase.com)
2. Faça login na sua conta
3. Selecione seu projeto FINS (ou crie um novo)

### Passo 2: Abra o SQL Editor
1. No menu lateral esquerdo, clique em **"SQL Editor"**
2. Clique em **"New query"**

### Passo 3: Execute o Script
1. Copie todo o conteúdo do arquivo `scripts/setup_database.sql`
2. Cole no editor SQL
3. Clique em **"Run"** (ou pressione Ctrl+Enter)

### Passo 4: Verifique a Execução
Após executar, você deve ver a mensagem:
```
Database setup completed successfully!
```

## Método 2: Via Script Python

### Pré-requisitos
1. Configure o arquivo `.env` com suas credenciais do Supabase
2. Instale as dependências: `pip install -r requirements.txt`

### Execução
```bash
cd fins-backend
python scripts/execute_setup.py
```

## Método 3: Via Supabase CLI

### Instalação do CLI
```bash
npm install -g supabase
```

### Login e Configuração
```bash
supabase login
supabase link --project-ref YOUR_PROJECT_ID
```

### Execução
```bash
cd fins-backend
supabase db reset
```

## Verificação do Setup

Após executar qualquer método, verifique se as tabelas foram criadas:

1. No Supabase Dashboard, vá para **"Table Editor"**
2. Você deve ver as seguintes tabelas:
   - `users`
   - `financial_profiles`
   - `expenses`
   - `receipts`

## Estrutura Criada

### Tabelas
- **users**: Dados dos usuários
- **financial_profiles**: Perfis financeiros
- **expenses**: Despesas registradas
- **receipts**: Recibos/entradas

### Funcionalidades
- ✅ Índices de performance
- ✅ Triggers para `updated_at`
- ✅ Políticas RLS (Row Level Security)
- ✅ Função `calculate_user_balance`
- ✅ View `financial_summary`

## Próximos Passos

Após o setup do banco:
1. Configure o arquivo `.env` com suas credenciais
2. Execute o backend: `python -m uvicorn app.main:app --reload`
3. Acesse a documentação: `http://localhost:8000/docs`

## Troubleshooting

### Erro: "permission denied"
- Use a **Service Key** (não a anon key) no arquivo `.env`
- Verifique se você tem permissões de admin no projeto

### Erro: "table already exists"
- O script usa `CREATE TABLE IF NOT EXISTS`, então é seguro executar múltiplas vezes

### Erro: "extension not found"
- O Supabase já tem as extensões necessárias habilitadas por padrão 