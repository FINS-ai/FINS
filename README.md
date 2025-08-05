# 🚀 FINS - Sistema de Gestão Financeira com IA

Sistema completo de gestão financeira pessoal com integração de IA para previsões e insights financeiros.

## 📁 Estrutura do Projeto

- **`fins-backend/`** - Backend em FastAPI com IA
- **`fins-frontend/`** - Frontend em React/TypeScript

## 🛠️ Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **Supabase** - Backend-as-a-Service
- **PostgreSQL** - Banco de dados relacional
- **JWT** - Autenticação segura
- **Pandas, NumPy, Scikit-learn, XGBoost, Prophet** - IA e análise de dados

### Frontend
- **React 18** - Biblioteca JavaScript para interfaces
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework CSS utilitário
- **React Router** - Roteamento
- **React Query** - Gerenciamento de estado do servidor
- **React Hook Form** - Formulários
- **Docker & Nginx** - Containerização e servidor web

## 🚀 Como Executar

### Backend
```bash
cd fins-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd fins-frontend
npm install
npm start
```

## 📖 Documentação

- [Backend README](fins-backend/README.md)
- [Frontend README](fins-frontend/README.md)
- [Quick Start Guide](fins-frontend/QUICKSTART.md)

## 🔧 Funcionalidades

### Backend
- ✅ Autenticação JWT
- ✅ Gestão de usuários
- ✅ Gestão financeira (despesas, receitas)
- ✅ Análise de IA (previsões, insights)
- ✅ API RESTful completa

### Frontend
- ✅ Interface moderna e responsiva
- ✅ Autenticação e registro
- ✅ Dashboard financeiro
- ✅ Gestão de despesas e receitas
- ✅ Integração com IA
- ✅ Design system consistente

## 🐳 Docker

Para executar com Docker:

```bash
# Backend
cd fins-backend
docker-compose up

# Frontend
cd fins-frontend
docker-compose up
```

## 📝 Licença

Este projeto está sob a licença MIT.

## 👥 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

Desenvolvido com ❤️ para a startup FINS 