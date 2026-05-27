from sqlalchemy import Column, String
from app.core.database import Base

class EventoProcessado(Base):
    __tablename__ = "eventos_processados"

    event_id = Column(String, primary_key=True, index=True)