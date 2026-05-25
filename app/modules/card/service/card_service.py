from app.database.repositories.card_repository import CardRepository
from app.modules.card.dto.update_card import UpdateCardDto
from app.modules.user.service.user_service import CustomerService
from fastapi import HTTPException, status

class CardService:
    def __init__(self, customer_service: CustomerService, card_repo: CardRepository):
        self.customer_service = customer_service
        self.card_repository = card_repo
        
    async def card_update(self, dto: UpdateCardDto):
        event_record = await self.card_repository.find_event_by_id(dto.event_id)

        if(event_record):
          raise HTTPException(
              status_code=status.HTTP_200_OK,
              detail=f"Evento ja registrado"
          )
        
        ownerEmail = await self.customer_service.find_customer_by_email(dto.cliente_email)

        if(not ownerEmail):
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Email {dto.cliente_email} não foi encontrado"
          )
        
        await self.card_repository.create(dto)