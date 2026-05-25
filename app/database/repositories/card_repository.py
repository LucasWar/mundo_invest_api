from sqlalchemy.ext.asyncio import AsyncSession
from app.models.evento_processado import EventoProcessado
from app.modules.card.dto.update_card import UpdateCardDto
from sqlalchemy import select 

class CardRepository:
  def __init__(self, db: AsyncSession):
        self.db = db

  async def create(self, dto: UpdateCardDto):
      new_card = EventoProcessado(
          event_id = dto.event_id
      )
      self.db.add(new_card)
      await self.db.commit()
      await self.db.refresh(new_card)

      return new_card
  
  async def find_event_by_id(self, id: str):
      stmt = select(EventoProcessado).where(EventoProcessado.event_id == id)
      result = await self.db.execute(stmt)
      event = result.scalar_one_or_none()

      return event