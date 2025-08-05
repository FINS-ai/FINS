from typing import List, Optional, Dict, Any
from supabase import Client
from app.models.user import FinancialProfile, FinancialProfileCreate, FinancialProfileUpdate, Expense, ExpenseCreate, ExpenseUpdate, Receipt, ReceiptCreate, ReceiptUpdate
from fastapi import HTTPException, status
import logging
from datetime import datetime, timedelta
import uuid
import json

logger = logging.getLogger(__name__)

class FinancialService:
    def __init__(self, db: Client):
        self.db = db
    
    # Financial Profile Methods
    async def create_financial_profile(self, profile_data: FinancialProfileCreate) -> FinancialProfile:
        """Cria um novo perfil financeiro"""
        try:
            profile_dict = profile_data.dict()
            profile_dict["id"] = str(uuid.uuid4())
            profile_dict["created_at"] = datetime.utcnow().isoformat()
            profile_dict["updated_at"] = datetime.utcnow().isoformat()
            
            # Converte monthly_expenses para JSON
            if profile_dict.get("monthly_expenses"):
                profile_dict["monthly_expenses"] = json.dumps(profile_dict["monthly_expenses"])
            
            result = self.db.table("financial_profiles").insert(profile_dict).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao criar perfil financeiro"
                )
            
            created_profile = result.data[0]
            # Converte JSON de volta para dict
            if created_profile.get("monthly_expenses"):
                created_profile["monthly_expenses"] = json.loads(created_profile["monthly_expenses"])
            
            return FinancialProfile(**created_profile)
            
        except Exception as e:
            logger.error(f"Erro ao criar perfil financeiro: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
    
    async def get_financial_profile(self, user_id: str) -> Optional[FinancialProfile]:
        """Busca perfil financeiro do usuário"""
        try:
            result = self.db.table("financial_profiles").select("*").eq("user_id", user_id).execute()
            
            if not result.data:
                return None
            
            profile = result.data[0]
            # Converte JSON de volta para dict
            if profile.get("monthly_expenses"):
                profile["monthly_expenses"] = json.loads(profile["monthly_expenses"])
            
            return FinancialProfile(**profile)
            
        except Exception as e:
            logger.error(f"Erro ao buscar perfil financeiro: {e}")
            return None
    
    async def update_financial_profile(self, user_id: str, profile_data: FinancialProfileUpdate) -> Optional[FinancialProfile]:
        """Atualiza perfil financeiro"""
        try:
            update_data = profile_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            # Converte monthly_expenses para JSON se existir
            if update_data.get("monthly_expenses"):
                update_data["monthly_expenses"] = json.dumps(update_data["monthly_expenses"])
            
            result = self.db.table("financial_profiles").update(update_data).eq("user_id", user_id).execute()
            
            if not result.data:
                return None
            
            profile = result.data[0]
            # Converte JSON de volta para dict
            if profile.get("monthly_expenses"):
                profile["monthly_expenses"] = json.loads(profile["monthly_expenses"])
            
            return FinancialProfile(**profile)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar perfil financeiro: {e}")
            return None
    
    # Expense Methods
    async def create_expense(self, expense_data: ExpenseCreate) -> Expense:
        """Cria uma nova despesa e atualiza o saldo"""
        try:
            expense_dict = expense_data.dict()
            expense_dict["id"] = str(uuid.uuid4())
            expense_dict["created_at"] = datetime.utcnow().isoformat()
            expense_dict["updated_at"] = datetime.utcnow().isoformat()
            
            # Insere a despesa
            result = self.db.table("expenses").insert(expense_dict).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao criar despesa"
                )
            
            # Atualiza o saldo do usuário
            await self._update_user_balance(expense_data.user_id, -expense_data.amount)
            
            return Expense(**result.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao criar despesa: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
    
    async def get_user_expenses(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Expense]:
        """Lista despesas do usuário"""
        try:
            result = self.db.table("expenses").select("*").eq("user_id", user_id).order("date", desc=True).range(skip, skip + limit).execute()
            
            return [Expense(**expense) for expense in result.data]
            
        except Exception as e:
            logger.error(f"Erro ao listar despesas: {e}")
            return []
    
    async def update_expense(self, expense_id: str, user_id: str, expense_data: ExpenseUpdate) -> Optional[Expense]:
        """Atualiza uma despesa"""
        try:
            # Busca a despesa atual para calcular a diferença
            current_expense = await self._get_expense_by_id(expense_id)
            if not current_expense:
                return None
            
            update_data = expense_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            result = self.db.table("expenses").update(update_data).eq("id", expense_id).eq("user_id", user_id).execute()
            
            if not result.data:
                return None
            
            # Atualiza o saldo se o valor mudou
            if "amount" in update_data:
                amount_diff = current_expense.amount - update_data["amount"]
                await self._update_user_balance(user_id, amount_diff)
            
            return Expense(**result.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao atualizar despesa: {e}")
            return None
    
    async def delete_expense(self, expense_id: str, user_id: str) -> bool:
        """Deleta uma despesa e atualiza o saldo"""
        try:
            # Busca a despesa para obter o valor
            current_expense = await self._get_expense_by_id(expense_id)
            if not current_expense:
                return False
            
            result = self.db.table("expenses").delete().eq("id", expense_id).eq("user_id", user_id).execute()
            
            if result.data:
                # Atualiza o saldo (adiciona o valor de volta)
                await self._update_user_balance(user_id, current_expense.amount)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao deletar despesa: {e}")
            return False
    
    # Receipt Methods
    async def create_receipt(self, receipt_data: ReceiptCreate) -> Receipt:
        """Cria um novo recibo e atualiza o saldo"""
        try:
            receipt_dict = receipt_data.dict()
            receipt_dict["id"] = str(uuid.uuid4())
            receipt_dict["created_at"] = datetime.utcnow().isoformat()
            receipt_dict["updated_at"] = datetime.utcnow().isoformat()
            
            # Insere o recibo
            result = self.db.table("receipts").insert(receipt_dict).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao criar recibo"
                )
            
            # Atualiza o saldo do usuário
            await self._update_user_balance(receipt_data.user_id, receipt_data.amount)
            
            return Receipt(**result.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao criar recibo: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
    
    async def get_user_receipts(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Receipt]:
        """Lista recibos do usuário"""
        try:
            result = self.db.table("receipts").select("*").eq("user_id", user_id).order("date", desc=True).range(skip, skip + limit).execute()
            
            return [Receipt(**receipt) for receipt in result.data]
            
        except Exception as e:
            logger.error(f"Erro ao listar recibos: {e}")
            return []
    
    # Helper Methods
    async def _update_user_balance(self, user_id: str, amount_change: float) -> bool:
        """Atualiza o saldo do usuário"""
        try:
            # Busca o perfil financeiro atual
            profile = await self.get_financial_profile(user_id)
            if not profile:
                return False
            
            new_balance = profile.current_balance + amount_change
            
            result = self.db.table("financial_profiles").update({
                "current_balance": new_balance,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("user_id", user_id).execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Erro ao atualizar saldo: {e}")
            return False
    
    async def _get_expense_by_id(self, expense_id: str) -> Optional[Expense]:
        """Busca despesa por ID"""
        try:
            result = self.db.table("expenses").select("*").eq("id", expense_id).execute()
            
            if not result.data:
                return None
            
            return Expense(**result.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao buscar despesa por ID: {e}")
            return None
    
    async def get_financial_summary(self, user_id: str) -> Dict[str, Any]:
        """Retorna resumo financeiro do usuário"""
        try:
            profile = await self.get_financial_profile(user_id)
            if not profile:
                return {}
            
            # Busca despesas dos últimos 30 dias
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            expenses_result = self.db.table("expenses").select("*").eq("user_id", user_id).gte("date", thirty_days_ago.isoformat()).execute()
            
            # Busca recibos dos últimos 30 dias
            receipts_result = self.db.table("receipts").select("*").eq("user_id", user_id).gte("date", thirty_days_ago.isoformat()).execute()
            
            total_expenses = sum(expense["amount"] for expense in expenses_result.data)
            total_receipts = sum(receipt["amount"] for receipt in receipts_result.data)
            
            return {
                "current_balance": profile.current_balance,
                "monthly_salary": profile.salary,
                "monthly_expenses": profile.monthly_expenses,
                "last_30_days_expenses": total_expenses,
                "last_30_days_receipts": total_receipts,
                "net_flow_30_days": total_receipts - total_expenses
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo financeiro: {e}")
            return {} 