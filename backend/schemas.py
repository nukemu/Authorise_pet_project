from pydantic import BaseModel
from datetime import datetime


class DiaryEntryBase(BaseModel):
    text: str
    
    
class DiaryEntryCreate(DiaryEntryBase):
    pass


class DiaryEntrySchemas(DiaryEntryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True