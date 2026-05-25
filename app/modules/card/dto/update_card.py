from pydantic import BaseModel, EmailStr, Field

class UpdateCardDto(BaseModel):
  event_id: str = Field(..., min_length=6, description="Idempotenci id")
  card_id: str = Field(..., description="card id")
  cliente_email: EmailStr = Field(..., description="Email pertencente ao cliente")
  timestamp: str = Field(..., description="Horário da requisição")