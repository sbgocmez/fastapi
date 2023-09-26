from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import FastAPI, Response, status, Request
from fastapi import HTTPException
from .. import models, schemas2
from ..database import engine, get_db
from typing import List

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/tracks", response_model=List[schemas2.TrackResponse])
def get_tracks(request: Request, db: Session=Depends(get_db)):
    client_host = request.client.host
    tracks = db.query(models.Track).all()
    print("---")
    print(client_host)
    return tracks

@router.post("/tracks", status_code=status.HTTP_201_CREATED, response_model=schemas2.TrackResponse)
def create_tracks(track: schemas2.CreateTrack, db: Session=Depends(get_db)):
    new_track = models.Track(**track.dict())
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    
    return new_track

@router.get("/tracks/{id}", response_model=schemas2.TrackResponse)
def get_track(id:int, db: Session=Depends(get_db)):
    track = db.query(models.Track).filter(models.Track.id == id).first()
    
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id {id}")
    
    return track


@router.delete("/tracks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_track(id:int, db: Session=Depends(get_db)):
    track_query = db.query(models.Track).filter(models.Track.id == id)
    
    track = track_query.first()
    
    if track == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id {id}")
    
    track_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/tracks/{id}", response_model=schemas.TrackResponse)
def update_track(id:int, track: schemas.CreateTrack, db: Session=Depends(get_db)):
    
    track_query = db.query(models.Track).filter(models.Track.id == id)
    track_to_update = track_query.first()
    
    if track_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found id to update")
    
    track_query.update(track.dict(), synchronize_session=False)
    db.commit()
    
    track_to_update = track_query.first()
    return track_to_update
