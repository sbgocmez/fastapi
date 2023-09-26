from fastapi import FastAPI
from .models import clientModel, visitModel
from .database import engine
from .routers import client
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import FastAPI, Response, status, Request
from fastapi import HTTPException
from .database import engine, get_db
from typing import List
from .models import clientModel
from .schemas import clientSchema

clientModel.Base.metadata.create_all(bind=engine)
visitModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], # get post put ?
    allow_headers=["*"],
)

@app.get("/")
def get_clients():
    return {"hello":"data"}

@app.get("/clients", response_model=List[clientSchema.ClientResponse])
def get_clients(request: Request, db: Session=Depends(get_db)):
    clients = db.query(clientModel.Client).all()
    return clients

@app.post("/clients", status_code=status.HTTP_201_CREATED, response_model=clientSchema.ClientResponse)
def create_client(request: Request, client: clientSchema.CreateClient, db: Session=Depends(get_db)):
    client.address = request.client.host
    new_client = clientModel.Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    
    return new_client

@app.get("/clients/{id}", response_model=clientSchema.ClientResponse)
def get_client(id:int, db: Session=Depends(get_db)):
    client = db.query(clientModel.Client).filter(clientModel.Client.id == id).first()
    
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id {id}")
    
    return client