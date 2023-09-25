from pydantic import BaseModel
# schemas

class TrackBase(BaseModel):
    device: str
    platform: str
    language: str

class CreateTrack(TrackBase):
    pass

