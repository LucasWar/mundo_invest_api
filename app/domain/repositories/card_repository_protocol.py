from app.modules.card.dto.update_card import UpdateCardDto
from typing import Protocol

class CardRepositoryProtocol(Protocol):

    async def card_update(self, dto: UpdateCardDto):
        ...
        
    async def find_event_by_id(self, id: str):
        ...