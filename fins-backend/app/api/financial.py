from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import (
    FinancialProfile, FinancialProfileCreate, FinancialProfileUpdate,
    Expense, ExpenseCreate, ExpenseUpdate, Receipt, ReceiptCreate, ReceiptUpdate
)
from app.services.financial_service import FinancialService
from app.auth.jwt import get_current_active_user
from app.database import get_db
from supabase import Client
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/financial", tags=["financeiro"])

# Financial Profile Endpoints
@router.post("/profile", response_model=FinancialProfile, status_code=status.HTTP_201_CREATED)
async def create_financial_profile(
    profile_data: FinancialProfileCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Cria um novo perfil financeiro para o usuário
    
    - **salary**: Salário mensal
    - **current_balance**: Saldo atual
    - **monthly_expenses**: Despesas mensais por categoria
    """
    try:
        # Verifica se o usuário já tem um perfil
        financial_service = FinancialService(db)
        existing_profile = await financial_service.get_financial_profile(current_user["user_id"])
        
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já possui um perfil financeiro"
            )
        
        # Cria o perfil
        profile_data.user_id = current_user["user_id"]
        profile = await financial_service.create_financial_profile(profile_data)
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar perfil financeiro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/profile", response_model=FinancialProfile)
async def get_financial_profile(
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Retorna o perfil financeiro do usuário atual
    """
    try:
        financial_service = FinancialService(db)
        profile = await financial_service.get_financial_profile(current_user["user_id"])
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil financeiro não encontrado"
            )
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar perfil financeiro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.put("/profile", response_model=FinancialProfile)
async def update_financial_profile(
    profile_data: FinancialProfileUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Atualiza o perfil financeiro do usuário
    
    - **salary**: Novo salário mensal (opcional)
    - **current_balance**: Novo saldo atual (opcional)
    - **monthly_expenses**: Novas despesas mensais (opcional)
    """
    try:
        financial_service = FinancialService(db)
        profile = await financial_service.update_financial_profile(current_user["user_id"], profile_data)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil financeiro não encontrado"
            )
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar perfil financeiro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# Expense Endpoints
@router.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Cria uma nova despesa
    
    - **amount**: Valor da despesa
    - **category**: Categoria da despesa
    - **description**: Descrição da despesa
    - **date**: Data da despesa
    """
    try:
        financial_service = FinancialService(db)
        expense_data.user_id = current_user["user_id"]
        expense = await financial_service.create_expense(expense_data)
        return expense
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar despesa: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/expenses", response_model=List[Expense])
async def get_expenses(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Lista todas as despesas do usuário
    
    - **skip**: Número de registros para pular
    - **limit**: Número máximo de registros
    """
    try:
        financial_service = FinancialService(db)
        expenses = await financial_service.get_user_expenses(current_user["user_id"], skip, limit)
        return expenses
        
    except Exception as e:
        logger.error(f"Erro ao listar despesas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.put("/expenses/{expense_id}", response_model=Expense)
async def update_expense(
    expense_id: str,
    expense_data: ExpenseUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Atualiza uma despesa específica
    
    - **expense_id**: ID da despesa
    - **amount**: Novo valor (opcional)
    - **category**: Nova categoria (opcional)
    - **description**: Nova descrição (opcional)
    - **date**: Nova data (opcional)
    """
    try:
        financial_service = FinancialService(db)
        expense = await financial_service.update_expense(expense_id, current_user["user_id"], expense_data)
        
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Despesa não encontrada"
            )
        
        return expense
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar despesa: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Deleta uma despesa específica
    
    - **expense_id**: ID da despesa
    """
    try:
        financial_service = FinancialService(db)
        success = await financial_service.delete_expense(expense_id, current_user["user_id"])
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Despesa não encontrada"
            )
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar despesa: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# Receipt Endpoints
@router.post("/receipts", response_model=Receipt, status_code=status.HTTP_201_CREATED)
async def create_receipt(
    receipt_data: ReceiptCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Cria um novo recibo
    
    - **amount**: Valor do recibo
    - **description**: Descrição do recibo
    - **date**: Data do recibo
    - **category**: Categoria (opcional)
    """
    try:
        financial_service = FinancialService(db)
        receipt_data.user_id = current_user["user_id"]
        receipt = await financial_service.create_receipt(receipt_data)
        return receipt
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar recibo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/receipts", response_model=List[Receipt])
async def get_receipts(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Lista todos os recibos do usuário
    
    - **skip**: Número de registros para pular
    - **limit**: Número máximo de registros
    """
    try:
        financial_service = FinancialService(db)
        receipts = await financial_service.get_user_receipts(current_user["user_id"], skip, limit)
        return receipts
        
    except Exception as e:
        logger.error(f"Erro ao listar recibos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# Summary Endpoint
@router.get("/summary", response_model=Dict[str, Any])
async def get_financial_summary(
    current_user: dict = Depends(get_current_active_user),
    db: Client = Depends(get_db)
):
    """
    Retorna um resumo financeiro do usuário
    
    Inclui:
    - Saldo atual
    - Salário mensal
    - Despesas mensais por categoria
    - Despesas dos últimos 30 dias
    - Recebimentos dos últimos 30 dias
    - Fluxo líquido dos últimos 30 dias
    """
    try:
        financial_service = FinancialService(db)
        summary = await financial_service.get_financial_summary(current_user["user_id"])
        
        if not summary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil financeiro não encontrado"
            )
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao gerar resumo financeiro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        ) 