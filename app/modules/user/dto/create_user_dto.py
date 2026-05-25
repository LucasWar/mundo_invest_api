from pydantic import BaseModel, EmailStr, Field

class CreateCustomerDto(BaseModel):
  cliente_nome: str = Field(..., min_length=2, description="Nome completo do cliente")
  cliente_email: EmailStr = Field(..., description="E-mail válido do cliente")
  tipo_solicitacao: str = Field(..., description="Tipo de solicitação no Pipefy")
  valor_patrimonio: float = Field(..., gt=0, description="Patrimônio deve ser maior que zero")