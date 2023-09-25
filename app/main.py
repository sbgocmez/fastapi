from fastapi import FastAPI, Response, status
from fastapi import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor


from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Track(BaseModel):
    device: str
    platform: str
    language: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tracks")
def get_tracks(db: Session=Depends(get_db)):
    tracks = db.query(models.Track).all()
    return {"[*] Tracks:": tracks}

@app.post("/tracks", status_code=status.HTTP_201_CREATED)
def create_tracks(track: Track, db: Session=Depends(get_db)):
    new_track = models.Track(**track.dict())
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    
    return {"[*] Created track": new_track}

@app.get("/tracks/{id}")
def get_track(id:int, db: Session=Depends(get_db)):
    track = db.query(models.Track).filter(models.Track.id == id).first()
    
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id {id}")
    
    return {f"[*] Track with id {id}":track}


@app.delete("/tracks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_track(id:int, db: Session=Depends(get_db)):
    track_query = db.query(models.Track).filter(models.Track.id == id)
    
    track = track_query.first()
    
    if track == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id {id}")
    
    track_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/tracks/{id}")
def update_track(id:int, track:Track, db: Session=Depends(get_db)):
    
    track_query = db.query(models.Track).filter(models.Track.id == id)
    track_to_update = track_query.first()
    
    if track_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found id to update")
    
    track_query.update(track.dict(), synchronize_session=False)
    db.commit()
    
    track_to_update = track_query.first()
    return {f"[*] Updated track with id {id}": track_to_update}