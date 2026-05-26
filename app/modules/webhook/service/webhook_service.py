from app.database.repositories.webhook_repository import WebhookRepository
from app.modules.webhook.dto.update_card import UpdateCardDto
from app.modules.customer.service.customer_service import CustomerService
from fastapi import HTTPException, status

class WebhookService:
    def __init__(self, customer_service: CustomerService, card_repo: WebhookRepository):
        self.customer_service = customer_service
        self.card_repository = card_repo
        
    async def card_update(self, dto: UpdateCardDto):
        event_record = await self.card_repository.find_event_by_id(dto.event_id)

        if(event_record):
          raise HTTPException(
              status_code=status.HTTP_200_OK,
              detail=f"Evento ja registrado"
          )
        
        customer = await self.customer_service.find_customer_by_email(dto.cliente_email)

        if(not customer):
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Email {dto.cliente_email} não foi encontrado"
          )
        
        prioridade = 'prioridade_normal'

        if(customer.valor_patrimonio >= 200000):
           prioridade = 'prioridade_alta'

        await self.customer_service.update_priority_record(dto.cliente_email, prioridade)

        await self.card_repository.create(dto)
        