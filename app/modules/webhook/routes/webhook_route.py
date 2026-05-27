from app.modules.webhook.dependecies import get_webhook_service
from app.modules.webhook.dto.update_card import UpdateCardDto
from fastapi import APIRouter, Depends, status
from app.modules.webhook.services.webhook_service import WebhookService

router = APIRouter()

@router.post("/webhooks/pipefy/card-updated", status_code=status.HTTP_200_OK)
async def read_root(dto: UpdateCardDto, service: WebhookService = Depends(get_webhook_service)):
    return await service.card_update(dto)