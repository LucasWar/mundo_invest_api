from app.modules.webhook.dependecies import get_webhook_service
from app.modules.webhook.dto.update_card import UpdateCardDto
from fastapi import APIRouter, Depends, status
from app.modules.webhook.service.webhook_service import WebhookService

router = APIRouter()

@router.post("/webhooks/pipefy/card-updated")
async def read_root(dto: UpdateCardDto, service: WebhookService = Depends(get_webhook_service), status_code=status.HTTP_200_OK):
    return await service.card_update(dto)