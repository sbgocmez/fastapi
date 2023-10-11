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
from datetime import datetime, timezone

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="app/templates")

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
    new_client.address = "159.5.37.64"
    new_client.device = "mobile"
    new_client.language = "en"
    new_client.platform = "andorid"
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return {"data":"Love you forever :)", "client":new_client}

@app.get("/clients", response_model=List[clientSchema.ClientResponse])
def get_clients(request: Request, db: Session=Depends(get_db)):
    clients = db.query(clientModel.Client).all()
    return clients

@app.get("/visits", response_model=List[clientSchema.VisitResponse])
def get_visits(request: Request, db: Session=Depends(get_db)):
    visits = db.query(visitModel.Visit).all()
    return visits


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
        new_visit.created_at = datetime.now(timezone.utc)
        
        print(new_visit.created_at)
        db.add(new_visit)
        db.commit()
        db.refresh(new_visit)
        
        print(new_visit.id)
        print(f"NOO PROBLEM UNTIL THERE {request_address}")
    
        existing_client.created_at = new_visit.created_at
        
        print(f" 22222 NOO PROBLEM UNTIL THERE {request_address}") 
        
        print(new_visit.created_at)
        
        db.commit()
        
        #last_visit = create_new_visit(existing_client.id)
        
        print(f"last visit for ip: {request_address} is at {new_visit.created_at}")
    else:
        print(f"This address does not exists in db {request_address}")
        client.address = request_address
        new_client = clientModel.Client(**client.dict())
        new_client
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        
        new_visit = visitModel.Visit()
        new_visit.client_id = new_client.id
        new_visit.created_at = datetime.now(timezone.utc)
        
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

@app.get("/visits/{id}", response_model=clientSchema.VisitResponse)
def get_visit(id:int, db: Session=Depends(get_db)):
    visit = db.query(visitModel.Visit).filter(visitModel.Visit.id == id).first()
    
    if not visit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id {id}")
    
    return visit

# @app.get("/deletetables")
# def delete_all( db: Session=Depends(get_db)):
#     for i in range(1,14):
#         # stm = visitModel.Visit.rem.where(visitModel.Visit.id == i)
#         # db.execute(stm)
#         # db.commit()
        
#         # # print(f" NOOOOOOOOO {i}")
#         vv = db.query(visitModel.Visit).filter(visitModel.Visit.id == i).first()
#         db.delete(vv)
#         db.commit()

@app.get('/analytics')      
def make_analytics(db: Session=Depends(get_db)):
    clients = db.query(clientModel.Client).all()
    my_data = []
    client_data = []
    
    #client_data = [{"id": client.id, "name": client.name, "email": client.email} for client in clients]
    for client in clients:
        if (True): # dummy olarak ekledigim icin.
            visit_list = db.query(visitModel.Visit).filter(visitModel.Visit.client_id == client.id).all()
            number_of_visits = len(visit_list)
            #print(datetime.now()-visit_list[0].created_at)
            formatted_date = client.created_at.strftime("%d.%m.%Y")
            client_data.append({"id":client.id, "address":client.address, "device":client.device, "platform":client.platform, "last visiting time":formatted_date, "total visits":number_of_visits})
            my_data.append({f"Client with IP address {client.address} visited the site {number_of_visits} time.\nClient platform {client.platform} and device {client.device}\nLast visit at {client.created_at}"})
    for data in client_data:
        print(data)
    return my_data

@app.get('/client-table', response_class=HTMLResponse)      
def make_analytics(request: Request, db: Session=Depends(get_db)):
    clients = db.query(clientModel.Client).all().sort(clientModel.Client.id)
    my_data = []
    client_data = []
    
    #client_data = [{"id": client.id, "name": client.name, "email": client.email} for client in clients]
    for client in clients:
        if (True): # dummy olarak ekledigim icin.
            visit_list = db.query(visitModel.Visit).filter(visitModel.Visit.client_id == client.id).all()
            number_of_visits = len(visit_list)
            #print(datetime.now()-visit_list[0].created_at)
            formatted_date = client.created_at.strftime("%d.%m.%Y")
            client_data.append({"id":client.id, "address":client.address, "device":client.device, "platform":client.platform,"last_visiting_time":formatted_date, "total_visits":number_of_visits})
            my_data.append({f"Client with IP address {client.address} visited the site {number_of_visits} time.\nClient platform {client.platform} and device {client.device}\nLast visit at {client.created_at}"})
    for data in client_data:
        print(data)
        
    return templates.TemplateResponse("client_table.html", {"request": request, "client_data": client_data})

@app.get('/delete-some')
def delete_some(db: Session=Depends(get_db)):
    client = db.query(clientModel.Client).filter(clientModel.Client.id == 5).first()
    #print(client.address)
    if client:
        print(client.address)
        db.delete(client)
        db.commit()
    else:
        print("Client with id not found")
    #db.query(clientModel.Client).delete(client)
    db.commit()
    #db.refresh()
    