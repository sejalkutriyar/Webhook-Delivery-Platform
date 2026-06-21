import uuid

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    subscriber_id = Column(UUID(as_uuid=True), ForeignKey("subscribers.id"), nullable=False)
    status = Column(String, default="pending")
    attempt_count = Column(Integer, default=0)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
