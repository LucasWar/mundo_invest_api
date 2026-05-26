from app.providers.card import get_card_service
from app.modules.card.dto.update_card import UpdateCardDto
from fastapi import APIRouter, Depends
from app.modules.card.service.card_service import CardService

router = APIRouter()

@router.post("/webhooks/pipefy/card-updated")
async def read_root(dto: UpdateCardDto, service: CardService = Depends(get_card_service)):
    return await service.card_update(dto)