from typing import List, Optional, Dict, Any
from supabase import Client
from app.models.user import User, UserCreate, UserUpdate
from app.auth.jwt import jwt_manager
from fastapi import HTTPException, status
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Client):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Cria um novo usuário"""
        try:
            # Verifica se o email já existe
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado"
                )
            
            # Gera hash da senha
            hashed_password = jwt_manager.get_password_hash(user_data.password)
            
            # Prepara dados do usuário
            user_dict = user_data.dict()
            user_dict.pop("password")
            user_dict["id"] = str(uuid.uuid4())
            user_dict["hashed_password"] = hashed_password
            user_dict["created_at"] = datetime.utcnow().isoformat()
            user_dict["updated_at"] = datetime.utcnow().isoformat()
            user_dict["is_active"] = True
            
            # Insere no banco
            result = self.db.table("users").insert(user_dict).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao criar usuário"
                )
            
            created_user = result.data[0]
            return User(**created_user)
            
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuário por ID"""
        try:
            result = self.db.table("users").select("*").eq("id", user_id).execute()
            
            if not result.data:
                return None
            
            return User(**result.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por ID: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        try:
            result = self.db.table("users").select("*").eq("email", email).execute()
            
            if not result.data:
                return None
            
            return User(**result.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por email: {e}")
            return None
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Atualiza dados do usuário"""
        try:
            update_data = user_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            result = self.db.table("users").update(update_data).eq("id", user_id).execute()
            
            if not result.data:
                return None
            
            return User(**result.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário: {e}")
            return None
    
    async def delete_user(self, user_id: str) -> bool:
        """Deleta usuário (soft delete)"""
        try:
            result = self.db.table("users").update({"is_active": False, "updated_at": datetime.utcnow().isoformat()}).eq("id", user_id).execute()
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Erro ao deletar usuário: {e}")
            return False
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Autentica usuário com email e senha"""
        try:
            user = await self.get_user_by_email(email)
            if not user:
                return None
            
            # Busca a senha hasheada
            result = self.db.table("users").select("hashed_password").eq("id", user.id).execute()
            if not result.data:
                return None
            
            hashed_password = result.data[0]["hashed_password"]
            
            if not jwt_manager.verify_password(password, hashed_password):
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Erro na autenticação: {e}")
            return None
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Lista todos os usuários ativos"""
        try:
            result = self.db.table("users").select("*").eq("is_active", True).range(skip, skip + limit).execute()
            
            return [User(**user) for user in result.data]
            
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {e}")
            return [] 