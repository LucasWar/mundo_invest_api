from fastapi import Depends
from app.database.database import get_db
from app.database.repositories.cutomer_repository import CustomerRepository
from app.modules.customer.service.customer_service import CustomerService

def get_customer_repository(db = Depends(get_db)):
    return CustomerRepository(db)

def get_customer_service(repo = Depends(get_customer_repository)):
    return CustomerService(repo)