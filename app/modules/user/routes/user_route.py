from app.dependencies.customer import get_customer_service
from app.modules.user.dto.create_user_dto import CreateCustomerDto
from app.modules.user.dto.customer_response_dto import CustomerResponseDto
from app.modules.user.service.user_service import CustomerService
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/clientes", response_model= CustomerResponseDto)
async def read_root(dto: CreateCustomerDto, service: CustomerService = Depends(get_customer_service)):
    return await service.criar_cliente(dto)