from app.domain.repositories.customer_repository_protocol import CustomerRepositoryProtocol
from app.modules.customer.dto.create_customer_dto import CreateCustomerDto
from fastapi import HTTPException, status

from app.modules.customer.dto.customer_response_dto import CustomerResponseDto

class CustomerService:
    def __init__(self, repo: CustomerRepositoryProtocol):
        self.repo = repo

    async def criar_cliente(self, dto: CreateCustomerDto) -> CustomerResponseDto:
        ownerEmail = await self.repo.find_customer_by_email(dto.cliente_email)

        if(ownerEmail):
          raise HTTPException(
              status_code=status.HTTP_409_CONFLICT,
              detail=f"O email {dto.cliente_email} já está sendo usado"
          )

        newCustomer = await self.repo.create(dto)
        
        await self.assemble_payload_card_mutatio(newCustomer)

        return CustomerResponseDto(
            id=newCustomer.id,
            cliente_nome=newCustomer.cliente_nome,
            cliente_email=newCustomer.cliente_email,
            status = newCustomer.status
        )
    
    async def find_customer_by_email(self, email: str): 
        customer = await self.repo.find_customer_by_email(email)

        return customer
    
    async def update_priority_record(self, email: str): 
        customer = await self.repo.find_customer_by_email(email)

        return customer

    async def assemble_payload_card_mutatio(self, customer: CreateCustomerDto):
        PIPE_ID = 12345678
        mutation_create_card = f"""
        mutation {{
        createCard(
            input: {{
            pipe_id: {PIPE_ID}
            fields_attributes: [
                {{field_id: "nome", field_value: "{customer.cliente_nome}"}}
                {{field_id: "email", field_value: "{customer.cliente_email}"}}
                {{field_id: "tipo_de_solicitacao", field_value: "{customer.tipo_solicitacao}"}}
                {{field_id: "patrimonio", field_value: "{customer.valor_patrimonio}"}}
            ]
            }}
        ) {{
            card {{ id title }}
        }}
        }}
        """
        print("Enviando para o Pipefy:\n", mutation_create_card)