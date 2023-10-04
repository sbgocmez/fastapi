from pydantic import BaseModel
from datetime import datetime
from fastapi.params import Optional

### requests

class ClientBase(BaseModel):
    device: Optional[str] = 'default'
    platform: Optional[str] = 'def platform'
    language: Optional[str] = 'def language'
    
class ClientResponse(ClientBase):
    id: int
    created_at: datetime
    address: str
    
    class Config:
        from_orm = True

# should be fixed
class CreateClient(ClientBase):
    address: Optional[str] = '.'
    
class VisitResponse(BaseModel):
    id: int
    created_at: datetime
    client_id: int
    
    class Config:
        from_orm = True

