from fastapi import FastAPI
from app.modules.user.routes import user_route
from app.modules.card.routes import card_route

app = FastAPI()

app.include_router(user_route.router)
app.include_router(card_route.router)