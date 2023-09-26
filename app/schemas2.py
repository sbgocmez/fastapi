from pydantic import BaseModel
from datetime import datetime
# schemas

class TrackBase(BaseModel):
    device: str
    platform: str
    language: str

class CreateTrack(TrackBase):
    pass

class TrackResponse(TrackBase):
    # id: int
    created_at: datetime
    
    class Config:
        from_orm = True
        
        
