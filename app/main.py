from fastapi import FastAPI
from .models import clientModel, visitModel
from .database import engine
from .routers import client
from fastapi.middleware.cors import CORSMiddleware

clientModel.Base.metadata.create_all(bind=engine)
visitModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins= ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # get post put ?
    allow_headers=["*"],
)
app.include_router(client.router)