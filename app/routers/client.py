from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import FastAPI, Response, status, Request
from fastapi import HTTPException
from ..models import clientModel
from ..schemas import clientSchema
from ..database import engine, get_db
from typing import List
from fastapi import APIRouter

router = APIRouter(
    tags=['Clients']
)

##### (REQUEST) VISITS 
@router.get("/", response_model=List[clientSchema.ClientResponse])
def get_clients(request: Request, db: Session=Depends(get_db)):
    clients = db.query(clientModel.Client).all()
    return clients
@router.get("/", response_model=List[clientSchema.ClientResponse])
def get_clients(request: Request, db: Session=Depends(get_db)):
    clients = db.query(clientModel.Client).all()
    return clients

@router.post("/clients", status_code=status.HTTP_201_CREATED, response_model=clientSchema.ClientResponse)
def create_client(request: Request, client: clientSchema.CreateClient, db: Session=Depends(get_db)):
    client.address = request.client.host
    new_client = clientModel.Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    
    return new_client

@router.get("/clients/{id}", response_model=clientSchema.ClientResponse)
def get_client(id:int, db: Session=Depends(get_db)):
    client = db.query(clientModel.Client).filter(clientModel.Client.id == id).first()
    
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id {id}")
    
    return client