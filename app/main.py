from fastapi import FastAPI
from .models import clientModel
from .database import engine
from .routers import client

clientModel.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(client.router)