from pydantic import BaseModel

class CustomerResponseDto(BaseModel):
    id: int
    cliente_nome: str
    cliente_email: str
    status: str

    class Config:
        from_attributes = True