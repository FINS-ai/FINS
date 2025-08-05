from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "FINS - Financial Intelligence System"
    version: str = "1.0.0"
    description: str = "Sistema de Inteligência Artificial para Auxílio Financeiro Pessoal"
    
    # CORS Configuration
    backend_cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Supabase Configuration
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""
    
    # JWT Configuration
    secret_key: str = "your-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database Configuration
    database_url: str = ""
    
    # ML Model Configuration
    model_path: str = "./models/"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignora campos extras nas variáveis de ambiente
        protected_namespaces = ('settings_',)

settings = Settings() 