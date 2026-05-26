from app.modules.customer.dependecies import get_customer_service
from app.modules.customer.dto.create_customer_dto import CreateCustomerDto
from app.modules.customer.dto.customer_response_dto import CustomerResponseDto
from app.modules.customer.service.customer_service import CustomerService
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/clientes", response_model= CustomerResponseDto)
async def read_root(dto: CreateCustomerDto, service: CustomerService = Depends(get_customer_service)):
    return await service.criar_cliente(dto)