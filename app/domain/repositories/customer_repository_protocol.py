from app.modules.customer.dto.customer_response_dto import CustomerResponseDto
from app.modules.customer.dto.create_customer_dto import CreateCustomerDto
from typing import Protocol

class CustomerRepositoryProtocol(Protocol):

    async def create(self, dto: CreateCustomerDto) -> CustomerResponseDto:
        ...

    async def find_customer_by_email(self, email: str) -> CustomerResponseDto | None:
        ...