# 🚀 FINS Frontend - Guia de Início Rápido

## Instalação Rápida

### Opção 1: Desenvolvimento Local

1. **Instalar dependências:**
```bash
npm install
```

2. **Configurar variáveis de ambiente:**
```bash
# Criar arquivo .env
echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > .env
```

3. **Iniciar o servidor de desenvolvimento:**
```bash
npm start
```

4. **Acessar a aplicação:**
   - Abra http://localhost:3000 no navegador
   - Certifique-se de que o backend está rodando na porta 8000

### Opção 2: Docker (Recomendado)

1. **Executar com Docker Compose:**
```bash
docker-compose up --build
```

2. **Acessar a aplicação:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentação API: http://localhost:8000/docs

## 🎯 Primeiros Passos

1. **Criar uma conta:**
   - Acesse http://localhost:3000
   - Clique em "Criar conta"
   - Preencha seus dados

2. **Fazer login:**
   - Use suas credenciais para acessar o dashboard

3. **Configurar perfil financeiro:**
   - Adicione seu salário e saldo atual
   - Configure suas despesas mensais

4. **Explorar funcionalidades:**
   - Dashboard com visão geral
   - Gestão de despesas e receitas
   - Insights de IA (em desenvolvimento)

## 🛠️ Scripts Úteis

```bash
# Desenvolvimento
npm start          # Inicia servidor de desenvolvimento
npm run build      # Gera build de produção
npm test           # Executa testes

# Docker
docker-compose up --build    # Inicia todos os serviços
docker-compose down          # Para todos os serviços
docker-compose logs -f       # Visualiza logs em tempo real
```

## 🔧 Configuração do Ambiente

### Variáveis de Ambiente (.env)

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1

# Environment
REACT_APP_ENV=development

# Feature Flags
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_DEBUG=true
```

### Pré-requisitos

- **Node.js 16+** e **npm**
- **Backend FINS** rodando na porta 8000
- **Navegador moderno** (Chrome, Firefox, Safari, Edge)

## 🐛 Solução de Problemas

### Erro de Conexão com API
- Verifique se o backend está rodando
- Confirme a URL da API no arquivo .env
- Verifique os logs do backend

### Erro de Build
```bash
# Limpar cache e reinstalar dependências
rm -rf node_modules package-lock.json
npm install
```

### Erro de Porta em Uso
```bash
# Encontrar processo usando a porta 3000
lsof -ti:3000
# Matar o processo
kill -9 <PID>
```

## 📱 Funcionalidades Disponíveis

### ✅ Implementadas
- ✅ Autenticação (login/registro)
- ✅ Dashboard responsivo
- ✅ Integração com APIs
- ✅ Design system moderno
- ✅ Navegação intuitiva

### 🚧 Em Desenvolvimento
- 🔄 Gestão de despesas/receitas
- 🔄 Relatórios e gráficos
- 🔄 Insights de IA
- 🔄 Perfil do usuário

## 🤝 Suporte

- **Documentação:** README.md
- **Issues:** GitHub Issues
- **Email:** suporte@fins.com

---

**🎉 Pronto!** Seu frontend FINS está configurado e funcionando! 