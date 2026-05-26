from app.domain.repositories.customer_repository_protocol import CustomerRepositoryProtocol
from app.modules.customer.dto.customer_response_dto import CustomerResponseDto
from app.modules.customer.dto.create_customer_dto import CreateCustomerDto
from app.integrations.pipefy.client import PipefyClient
from fastapi import HTTPException, status
from typing import Literal


class CustomerService:
    def __init__(self, repo: CustomerRepositoryProtocol, pipefy_client: PipefyClient):
        self.repo = repo
        self.pipefy_client = pipefy_client

    async def criar_cliente(self, dto: CreateCustomerDto) -> CustomerResponseDto:
        ownerEmail = await self.repo.find_customer_by_email(dto.cliente_email)

        if(ownerEmail):
          raise HTTPException(
              status_code=status.HTTP_409_CONFLICT,
              detail=f"O email {dto.cliente_email} já está sendo usado"
          )

        newCustomer = await self.repo.create(dto)
        
        await self.pipefy_client.create_card(newCustomer)

        return CustomerResponseDto(
            id=newCustomer.id,
            cliente_nome=newCustomer.cliente_nome,
            cliente_email=newCustomer.cliente_email,
            status = newCustomer.status,
            valor_patrimonio = newCustomer.valor_patrimonio
        )
    
    async def find_customer_by_email(self, email: str): 
        customer = await self.repo.find_customer_by_email(email)

        return customer
    
    async def update_priority_record(self, email: str, new_priority: Literal["prioridade_alta", "prioridade_normal"]): 
        customer = await self.repo.find_customer_by_email(email)
        
        if(not customer):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"O email {email} não foi encontrado"
            )
        
        await self.repo.update_priority(customer.cliente_email,new_priority)