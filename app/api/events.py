from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.event import Event
from app.models.subscriber import Subscriber
from app.models.delivery import Delivery
from app.schemas.event import EventCreate, EventOut
from app.workers.delivery_worker import deliver_webhook

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventOut)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(event_type=event.event_type, payload=event.payload)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    subscribers = db.query(Subscriber).filter(Subscriber.is_active == True).all()
    for subscriber in subscribers:
        delivery = Delivery(event_id=db_event.id, subscriber_id=subscriber.id)
        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        deliver_webhook.delay(str(delivery.id))

    return db_event


@router.get("/", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.created_at.desc()).limit(50).all()
