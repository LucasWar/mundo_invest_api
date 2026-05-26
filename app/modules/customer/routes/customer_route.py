from app.domain.dto.customer.create_customer_response import CreateCustomerResponseDto
from app.modules.customer.dto.create_customer_dto import CreateCustomerDto
from app.modules.customer.service.customer_service import CustomerService
from app.modules.customer.dependecies import get_customer_service
from fastapi import APIRouter, Depends, status

router = APIRouter()

@router.post("/clientes", response_model = CreateCustomerResponseDto, status_code=status.HTTP_201_CREATED)
async def read_root(dto: CreateCustomerDto, service: CustomerService = Depends(get_customer_service)):
    return await service.create_customer(dto)