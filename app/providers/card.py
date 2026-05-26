from fastapi import Depends
from app.database.database import get_db
from app.database.repositories.card_repository import CardRepository
from app.providers.customer import get_customer_service 
from app.modules.card.service.card_service import CardService
from app.modules.customer.service.customer_service import CustomerService

def get_card_repository(db = Depends(get_db)):
    return CardRepository(db)

def get_card_service(customer_service: CustomerService = Depends(get_customer_service), card_repo = Depends(get_card_repository)) -> CardService:
    return CardService(customer_service, card_repo)