from app.modules.customer.dto.customer_response_dto import CustomerResponseDto
from app.modules.customer.dto.create_customer_dto import CreateCustomerDto
from app.modules.customer.models.cliente import Cliente
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select 
from sqlalchemy import update
from typing import Literal

class CustomerRepository:
  def __init__(self, db: AsyncSession):
        self.db = db

  async def create(self, dto: CreateCustomerDto):
    try:
      novo_cliente = Cliente(
          cliente_nome=dto.cliente_nome,
          cliente_email=dto.cliente_email,
          tipo_solicitacao=dto.tipo_solicitacao,
          valor_patrimonio=dto.valor_patrimonio,
          status="Aguardando Análise"
      )
      self.db.add(novo_cliente)
      await self.db.commit()
      await self.db.refresh(novo_cliente)

      return novo_cliente
    except SQLAlchemyError as e:
      await self.db.rollback()
      print(f"Erro de banco de dados: {e}")
      raise Exception("Falha ao criar o cliente no banco de dados")
    
  async def find_customer_by_email(self, email: str) -> CustomerResponseDto | None:
    try:
      stmt = select(Cliente).where(Cliente.cliente_email == email)
      result = await self.db.execute(stmt)
      customer = result.scalar_one_or_none()
      if(customer):
        return CustomerResponseDto(
          id=customer.id,
          cliente_nome=customer.cliente_nome,
          cliente_email=customer.cliente_email,
          status = customer.status,
          valor_patrimonio = customer.valor_patrimonio
        )
      else: 
         return None
    except SQLAlchemyError as e:
      await self.db.rollback()
      print(f"Erro de banco de dados: {e}")
      raise Exception("Falha ao encontrar o cliente no banco de dados")
    
  async def update_priority(self, email: str, new_priority: Literal["prioridade_alta", "prioridade_normal"]):
    try:
      await self.db.execute(
          update(Cliente).where(Cliente.cliente_email == email).values(
            prioridade = new_priority,
            status = "Processado"          
          )
      )
      await self.db.commit()

    except SQLAlchemyError as e:
      await self.db.rollback()
      print(f"Erro de banco de dados: {e}")