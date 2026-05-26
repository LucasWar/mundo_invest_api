# CreateCustomerResponseDto
from pydantic import BaseModel, ConfigDict

class CreateCustomerResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_email: str
    cliente_nome: str
    status: str
    valor_patrimonio: float