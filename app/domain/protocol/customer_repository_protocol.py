from app.domain.dto.customer.find_customer_by_email_response import FindCustomerByEmailResponse
from app.modules.customer.dto.create_customer_dto import CreateCustomerDto
from app.modules.customer.models.cliente import Cliente
from typing import Literal, Protocol


class CustomerRepositoryProtocol(Protocol):

    async def create(self, dto: CreateCustomerDto) -> Cliente:
        ...

    async def find_customer_by_email(self, email: str) -> Cliente | None:
        ...

    async def update_priority(self, email: str, new_priority: Literal["prioridade_alta", "prioridade_normal"]):
        ...