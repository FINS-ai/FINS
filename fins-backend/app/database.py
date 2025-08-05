from supabase import create_client, Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.supabase: Client = None
        self._connect()
    
    def _connect(self):
        """Estabelece conexão com o Supabase"""
        try:
            self.supabase = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
            logger.info("Conexão com Supabase estabelecida com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar com Supabase: {e}")
            raise
    
    def get_client(self) -> Client:
        """Retorna o cliente Supabase"""
        if not self.supabase:
            self._connect()
        return self.supabase

# Instância global do banco de dados
db = Database()

def get_db() -> Client:
    """Dependency para injetar o cliente do banco de dados"""
    return db.get_client() 