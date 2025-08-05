from fastapi import APIRouter, Depends, HTTPException, status
from app.models.ai_models import (
    BalancePrediction, SavingsPrediction, RiskAnalysis, 
    ExpenseAnalysis, FinancialInsights
)
from app.services.ai_service import AIService
from app.auth.jwt import get_current_active_user
from app.database import get_db
from supabase import Client
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["inteligência artificial"])

@router.get("/predict/balance", response_model=BalancePrediction)
async def predict_balance(
    months_ahead: int = 3,
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Previsão do saldo futuro
    
    - **months_ahead**: Número de meses para prever (padrão: 3)
    
    Retorna:
    - Saldo previsto
    - Intervalo de confiança
    - Data da previsão
    - Acurácia do modelo
    """
    try:
        ai_service = AIService(db)
        prediction = await ai_service.predict_balance(current_user["user_id"], months_ahead)
        return prediction
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro na previsão de saldo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/predict/savings", response_model=SavingsPrediction)
async def predict_savings(
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Previsão da capacidade de poupança
    
    Retorna:
    - Potencial de poupança mensal
    - Potencial de poupança anual
    - Taxa de poupança
    - Recomendações para aumentar poupança
    """
    try:
        ai_service = AIService(db)
        prediction = await ai_service.predict_savings(current_user["user_id"])
        return prediction
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro na previsão de poupança: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/analyze/risk", response_model=RiskAnalysis)
async def analyze_risk(
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Análise de risco de inadimplência
    
    Retorna:
    - Nível de risco (baixo, médio, alto, crítico)
    - Pontuação de risco (0-100)
    - Probabilidade de inadimplência
    - Fatores de risco identificados
    - Recomendações para reduzir risco
    """
    try:
        ai_service = AIService(db)
        analysis = await ai_service.analyze_risk(current_user["user_id"])
        return analysis
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro na análise de risco: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/analyze/expenses", response_model=ExpenseAnalysis)
async def analyze_expenses(
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Análise detalhada de despesas
    
    Retorna:
    - Total de despesas mensais
    - Despesas por categoria
    - Tendência das despesas
    - Despesas incomuns detectadas
    - Recomendações de orçamento
    """
    try:
        ai_service = AIService(db)
        analysis = await ai_service.analyze_expenses(current_user["user_id"])
        return analysis
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro na análise de despesas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/insights", response_model=FinancialInsights)
async def get_financial_insights(
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Insights financeiros completos
    
    Retorna uma análise completa incluindo:
    - Previsão de saldo
    - Previsão de poupança
    - Análise de risco
    - Análise de despesas
    - Pontuação geral de saúde financeira
    - Insights principais
    - Itens de ação recomendados
    """
    try:
        ai_service = AIService(db)
        insights = await ai_service.generate_financial_insights(current_user["user_id"])
        return insights
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro ao gerar insights financeiros: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/health", response_model=Dict[str, Any])
async def ai_health_check(
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Verificação de saúde dos modelos de IA
    
    Retorna:
    - Status dos modelos
    - Informações sobre dados disponíveis
    - Capacidades de análise
    """
    try:
        ai_service = AIService(db)
        
        # Verifica se o usuário tem dados suficientes
        df = await ai_service.get_user_financial_data(current_user["user_id"])
        
        health_status = {
            "status": "healthy",
            "user_id": current_user["user_id"],
            "data_available": not df.empty,
            "data_points": len(df) if not df.empty else 0,
            "date_range": {
                "start": df['date'].min().strftime('%Y-%m-%d') if not df.empty else None,
                "end": df['date'].max().strftime('%Y-%m-%d') if not df.empty else None
            },
            "capabilities": {
                "balance_prediction": not df.empty and len(df) >= 10,
                "savings_prediction": not df.empty and len(df) >= 5,
                "risk_analysis": not df.empty and len(df) >= 3,
                "expense_analysis": not df.empty and len(df[df['amount'] < 0]) >= 3
            },
            "models_ready": {
                "prophet": True,
                "xgboost": True,
                "random_forest": True
            }
        }
        
        return health_status
        
    except Exception as e:
        logger.error(f"Erro no health check de IA: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "user_id": current_user["user_id"]
        } 