from app.modules.customer.dto.customer_response_dto import CustomerResponseDto
from app.modules.customer.dto.create_customer_dto import CreateCustomerDto
from typing import Literal, Protocol

class CustomerRepositoryProtocol(Protocol):

    async def create(self, dto: CreateCustomerDto) -> CustomerResponseDto:
        ...

    async def find_customer_by_email(self, email: str) -> CustomerResponseDto | None:
        ...

    async def update_priority(self, email: str, new_priority: Literal["prioridade_alta", "prioridade_normal"]):
        ...