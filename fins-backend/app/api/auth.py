from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.auth.jwt import jwt_manager, get_current_active_user
from app.database import get_db
from supabase import Client
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["autenticação"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Client = Depends(get_db)):
    """
    Registra um novo usuário
    
    - **email**: Email único do usuário
    - **full_name**: Nome completo
    - **password**: Senha (mínimo 8 caracteres)
    - **phone**: Telefone (opcional)
    """
    try:
        user_service = UserService(db)
        user = await user_service.create_user(user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Client = Depends(get_db)):
    """
    Autentica usuário e retorna token JWT
    
    - **username**: Email do usuário
    - **password**: Senha do usuário
    """
    try:
        user_service = UserService(db)
        user = await user_service.authenticate_user(form_data.username, form_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Cria token de acesso
        access_token = jwt_manager.create_access_token(
            data={"sub": user.id, "email": user.email}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user), db: Client = Depends(get_db)):
    """
    Retorna informações do usuário atual
    """
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_id(current_user["user_id"])
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar usuário: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.put("/me", response_model=User)
async def update_current_user(
    user_data: UserUpdate, 
    current_user: dict = Depends(get_current_active_user), 
    db: Client = Depends(get_db)
):
    """
    Atualiza informações do usuário atual
    
    - **full_name**: Novo nome completo (opcional)
    - **phone**: Novo telefone (opcional)
    """
    try:
        user_service = UserService(db)
        updated_user = await user_service.update_user(current_user["user_id"], user_data)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return updated_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user: dict = Depends(get_current_active_user), 
    db: Client = Depends(get_db)
):
    """
    Deleta o usuário atual (soft delete)
    """
    try:
        user_service = UserService(db)
        success = await user_service.delete_user(current_user["user_id"])
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar usuário: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/users", response_model=List[User])
async def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Lista todos os usuários (apenas para administradores)
    """
    try:
        user_service = UserService(db)
        users = await user_service.get_all_users(skip, limit)
        return users
        
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        ) 