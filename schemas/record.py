from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.record import RecordType

class RecordBase(BaseModel):
    amount: float
    record_type: RecordType
    category: str
    notes: Optional[str] = None
    date: Optional[datetime] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    record_type: Optional[RecordType] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    date: Optional[datetime] = None

class RecordResponse(RecordBase):
    id: int
    author_id: int
    date: datetime

    class Config:
        from_attributes = True
