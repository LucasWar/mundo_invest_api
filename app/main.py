from fastapi import FastAPI
from app.modules.customer.routes import customer_route
from app.modules.card.routes import card_route

app = FastAPI()

app.include_router(customer_route.router)
app.include_router(card_route.router)