from pydantic import BaseModel, ConfigDict

class FindCustomerByEmailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_email: str
    cliente_nome: str
    status: str
    valor_patrimonio: float