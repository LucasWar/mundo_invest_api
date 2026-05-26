from fastapi import FastAPI
from app.modules.customer.routes import customer_route
from app.modules.webhook.routes import webhook_route

app = FastAPI()

app.include_router(customer_route.router)
app.include_router(webhook_route.router)