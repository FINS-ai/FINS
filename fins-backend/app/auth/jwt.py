from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Configuração de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do bearer token
security = HTTPBearer()

class JWTManager:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se a senha está correta"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Gera hash da senha"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Cria token de acesso JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verifica e decodifica o token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            logger.error(f"Erro ao verificar token: {e}")
            return None

# Instância global do JWT Manager
jwt_manager = JWTManager()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Dependency para obter o usuário atual baseado no token JWT"""
    token = credentials.credentials
    payload = jwt_manager.verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"user_id": user_id, "email": payload.get("email")}

async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency para obter usuário ativo"""
    # Aqui você pode adicionar lógica adicional para verificar se o usuário está ativo
    return current_user 