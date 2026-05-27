from fastapi import Depends
from app.core.database import get_db
from app.modules.webhook.repositories.webhook_repository import WebhookRepository
from app.modules.customer.dependecies import get_customer_service 
from app.modules.webhook.services.webhook_service import WebhookService
from app.modules.customer.services.customer_service import CustomerService

def get_webhook_repository(db = Depends(get_db)):
    return WebhookRepository(db)

def get_webhook_service(customer_service: CustomerService = Depends(get_customer_service), webhook_repo = Depends(get_webhook_repository)) -> WebhookService:
    return WebhookService(customer_service, webhook_repo)