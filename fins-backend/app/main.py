from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api import auth, financial, ai
import logging
import uvicorn

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Criação da aplicação FastAPI
app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers
app.include_router(auth.router, prefix=settings.api_v1_str)
app.include_router(financial.router, prefix=settings.api_v1_str)
app.include_router(ai.router, prefix=settings.api_v1_str)

# Middleware para tratamento de erros
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

# Endpoints de health check
@app.get("/")
async def root():
    """
    Endpoint raiz da API FINS
    """
    return {
        "message": "Bem-vindo à API FINS - Financial Intelligence System",
        "version": settings.version,
        "docs": "/docs",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """
    Verificação de saúde da API
    """
    return {
        "status": "healthy",
        "service": "FINS API",
        "version": settings.version
    }

@app.get("/info")
async def api_info():
    """
    Informações sobre a API
    """
    return {
        "name": settings.project_name,
        "description": settings.description,
        "version": settings.version,
        "endpoints": {
            "auth": f"{settings.api_v1_str}/auth",
            "financial": f"{settings.api_v1_str}/financial",
            "ai": f"{settings.api_v1_str}/ai"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 