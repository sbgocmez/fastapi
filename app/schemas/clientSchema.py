from pydantic import BaseModel
from datetime import datetime
from fastapi.params import Optional

### requests

class ClientBase(BaseModel):
    device: str
    platform: str
    language: str
    
class ClientResponse(ClientBase):
    id: int
    created_at: datetime
    address: str
    
    class Config:
        from_orm = True

# should be fixed
class CreateClient(ClientBase):
    address: Optional[str] = '.'