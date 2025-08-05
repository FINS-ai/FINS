-- Script de configuração inicial do banco de dados FINS
-- Execute este script no seu projeto Supabase

-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de perfis financeiros
CREATE TABLE IF NOT EXISTS financial_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    salary DECIMAL(10,2) NOT NULL CHECK (salary > 0),
    current_balance DECIMAL(10,2) NOT NULL,
    monthly_expenses JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Tabela de despesas
CREATE TABLE IF NOT EXISTS expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de recibos
CREATE TABLE IF NOT EXISTS receipts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    description VARCHAR(255) NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_financial_profiles_user_id ON financial_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);
CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category);
CREATE INDEX IF NOT EXISTS idx_receipts_user_id ON receipts(user_id);
CREATE INDEX IF NOT EXISTS idx_receipts_date ON receipts(date);

-- Função para atualizar o timestamp updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para atualizar updated_at automaticamente
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_financial_profiles_updated_at BEFORE UPDATE ON financial_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_expenses_updated_at BEFORE UPDATE ON expenses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_receipts_updated_at BEFORE UPDATE ON receipts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Políticas de segurança RLS (Row Level Security)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE receipts ENABLE ROW LEVEL SECURITY;

-- Políticas para usuários
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- Políticas para perfis financeiros
CREATE POLICY "Users can view own financial profile" ON financial_profiles
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own financial profile" ON financial_profiles
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own financial profile" ON financial_profiles
    FOR UPDATE USING (auth.uid()::text = user_id::text);

-- Políticas para despesas
CREATE POLICY "Users can view own expenses" ON expenses
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own expenses" ON expenses
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own expenses" ON expenses
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own expenses" ON expenses
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Políticas para recibos
CREATE POLICY "Users can view own receipts" ON receipts
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own receipts" ON receipts
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own receipts" ON receipts
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own receipts" ON receipts
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Função para calcular saldo total
CREATE OR REPLACE FUNCTION calculate_user_balance(user_uuid UUID)
RETURNS DECIMAL AS $$
DECLARE
    profile_balance DECIMAL;
    total_expenses DECIMAL;
    total_receipts DECIMAL;
BEGIN
    -- Obter saldo do perfil
    SELECT current_balance INTO profile_balance
    FROM financial_profiles
    WHERE user_id = user_uuid;
    
    IF profile_balance IS NULL THEN
        RETURN 0;
    END IF;
    
    -- Calcular total de despesas
    SELECT COALESCE(SUM(amount), 0) INTO total_expenses
    FROM expenses
    WHERE user_id = user_uuid;
    
    -- Calcular total de recibos
    SELECT COALESCE(SUM(amount), 0) INTO total_receipts
    FROM receipts
    WHERE user_id = user_uuid;
    
    RETURN profile_balance - total_expenses + total_receipts;
END;
$$ LANGUAGE plpgsql;

-- View para resumo financeiro
CREATE OR REPLACE VIEW financial_summary AS
SELECT 
    u.id as user_id,
    u.email,
    u.full_name,
    fp.salary,
    fp.current_balance,
    fp.monthly_expenses,
    calculate_user_balance(u.id) as calculated_balance,
    COALESCE(SUM(CASE WHEN e.date >= NOW() - INTERVAL '30 days' THEN e.amount ELSE 0 END), 0) as last_30_days_expenses,
    COALESCE(SUM(CASE WHEN r.date >= NOW() - INTERVAL '30 days' THEN r.amount ELSE 0 END), 0) as last_30_days_receipts
FROM users u
LEFT JOIN financial_profiles fp ON u.id = fp.user_id
LEFT JOIN expenses e ON u.id = e.user_id
LEFT JOIN receipts r ON u.id = r.user_id
WHERE u.is_active = true
GROUP BY u.id, u.email, u.full_name, fp.salary, fp.current_balance, fp.monthly_expenses;

-- Comentários nas tabelas
COMMENT ON TABLE users IS 'Tabela de usuários do sistema FINS';
COMMENT ON TABLE financial_profiles IS 'Perfis financeiros dos usuários';
COMMENT ON TABLE expenses IS 'Despesas registradas pelos usuários';
COMMENT ON TABLE receipts IS 'Recibos/entradas registradas pelos usuários';
COMMENT ON FUNCTION calculate_user_balance IS 'Calcula o saldo atual do usuário considerando despesas e recibos';
COMMENT ON VIEW financial_summary IS 'View com resumo financeiro dos usuários';

-- Inserir dados de exemplo (opcional - remova em produção)
-- INSERT INTO users (email, full_name, hashed_password) VALUES 
-- ('admin@fins.com', 'Administrador', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.i8Hy');

-- Mensagem de confirmação
SELECT 'Database setup completed successfully!' as status; 