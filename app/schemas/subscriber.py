import uuid

from pydantic import BaseModel


class SubscriberCreate(BaseModel):
    target_url: str


class SubscriberOut(BaseModel):
    id: uuid.UUID
    target_url: str
    is_active: bool

    class Config:
        from_attributes = True
