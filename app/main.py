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

origins= ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # get post put ?
    allow_headers=["*"],
)

@app.get("/")
def get_clients(request: Request, db: Session=Depends(get_db)):
    new_client = clientModel.Client()
    new_client.address = request.client.host
    new_client.device = "dummy"
    new_client.language = "dummy"
    new_client.platform = "dummy"
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return {"data":"Love you forever :)", "client":new_client}

@app.get("/clients", response_model=List[clientSchema.ClientResponse])
def get_clients(request: Request, db: Session=Depends(get_db)):
    clients = db.query(clientModel.Client).all()
    return clients


def create_new_visit(cid:int, db: Session=Depends(get_db)):
    new_visit = visitModel.Visit()
    new_visit.client_id = cid
    
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit
    
    
@app.post("/clients", status_code=status.HTTP_201_CREATED)
def create_client(request: Request, client: clientSchema.CreateClient, db: Session=Depends(get_db)):
    
    # if client.platform == "iOS" or client.platform == "MacOS" :
    #     new_client = visitModel.Client()
    #     new_client.address = "0.0.0.0"
    #     new_client.platform = "ios/macos"
    #     new_client.language = "--"
    #     new_client.device = "iphone/macos"
        
    #     db.add(new_client)
    #     db.commit()
    #     db.refresh(new_client)
        
    #     return {"some osx device"}
    request_address = request.client.host
    existing_client = db.query(clientModel.Client).filter(clientModel.Client.address == request_address).first()
    
    if ((existing_client != None)):
        print(f"This address already exists {request_address}")
        
        new_visit = visitModel.Visit()
        new_visit.client_id = existing_client.id
        
        db.add(new_visit)
        db.commit()
        db.refresh(new_visit)
    
        existing_client.created_at = new_visit.created_at
        db.commit()
        
        #last_visit = create_new_visit(existing_client.id)
        
        print(f"last visit for ip: {request_address} is at {new_visit.created_at}")
    else:
        print(f"This address does not exists in db {request_address}")
        client.address = request_address
        new_client = clientModel.Client(**client.dict())
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        
        new_visit = visitModel.Visit()
        new_visit.client_id = new_client.address
        
        db.add(new_visit)
        db.commit()
        db.refresh(new_visit)
    
    return {"new_":new_visit}

@app.get("/clients/{id}", response_model=clientSchema.ClientResponse)
def get_client(id:int, db: Session=Depends(get_db)):
    client = db.query(clientModel.Client).filter(clientModel.Client.id == id).first()
    
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id {id}")
    
    return client