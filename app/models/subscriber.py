import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_url = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
