# FINS Frontend

Frontend moderno e responsivo para a startup FINS (Financial Intelligence System), desenvolvido em React com TypeScript.

## 🚀 Tecnologias

- **React 18** - Biblioteca JavaScript para interfaces
- **TypeScript** - Tipagem estática para JavaScript
- **Tailwind CSS** - Framework CSS utilitário
- **React Router** - Roteamento da aplicação
- **React Query** - Gerenciamento de estado do servidor
- **React Hook Form** - Formulários performáticos
- **Lucide React** - Ícones modernos
- **Recharts** - Gráficos e visualizações
- **Framer Motion** - Animações suaves
- **Axios** - Cliente HTTP

## 📋 Pré-requisitos

- Node.js 16+ 
- npm ou yarn
- Backend FINS rodando na porta 8000

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd fins-frontend
```

2. Instale as dependências:
```bash
npm install
# ou
yarn install
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

4. Inicie o servidor de desenvolvimento:
```bash
npm start
# ou
yarn start
```

A aplicação estará disponível em `http://localhost:3000`

## 🏗️ Estrutura do Projeto

```
src/
├── components/          # Componentes React
│   ├── Auth/           # Componentes de autenticação
│   ├── Dashboard/      # Componentes do dashboard
│   ├── Layout/         # Componentes de layout
│   └── UI/             # Componentes de interface
├── contexts/           # Contextos React
├── services/           # Serviços de API
├── types/              # Definições TypeScript
├── utils/              # Utilitários
└── App.tsx            # Componente principal
```

## 🎨 Funcionalidades

### ✅ Implementadas
- **Autenticação completa** (login/registro)
- **Dashboard responsivo** com visão geral financeira
- **Integração com APIs** do backend
- **Design system** consistente
- **Navegação intuitiva**
- **Formatação de dados** (moeda, datas, etc.)

### 🚧 Em Desenvolvimento
- Gestão de despesas e receitas
- Relatórios e gráficos
- Insights de IA
- Perfil do usuário
- Configurações

## 🔧 Scripts Disponíveis

- `npm start` - Inicia o servidor de desenvolvimento
- `npm build` - Gera build de produção
- `npm test` - Executa os testes
- `npm eject` - Ejecta do Create React App

## 🌐 Integração com Backend

O frontend se integra com as seguintes APIs do backend:

- **Autenticação**: `/api/v1/auth/*`
- **Perfil Financeiro**: `/api/v1/financial/profile`
- **Despesas**: `/api/v1/financial/expenses`
- **Receitas**: `/api/v1/financial/receipts`
- **Resumo Financeiro**: `/api/v1/financial/summary`
- **IA Insights**: `/api/v1/ai/*`

## 🎯 Próximos Passos

1. **Implementar páginas de gestão financeira**
   - Adicionar/editar despesas
   - Adicionar/editar receitas
   - Categorização automática

2. **Desenvolver relatórios avançados**
   - Gráficos de tendências
   - Análise por categoria
   - Comparativos mensais

3. **Integrar insights de IA**
   - Previsões de saldo
   - Análise de risco
   - Recomendações personalizadas

4. **Melhorar UX/UI**
   - Animações mais fluidas
   - Modo escuro
   - PWA capabilities

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte, envie um email para suporte@fins.com ou abra uma issue no repositório. 