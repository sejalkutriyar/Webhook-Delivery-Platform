import uuid
from datetime import datetime

from pydantic import BaseModel


class EventCreate(BaseModel):
    event_type: str
    payload: dict


class EventOut(BaseModel):
    id: uuid.UUID
    event_type: str
    payload: dict
    created_at: datetime

    class Config:
        from_attributes = True
