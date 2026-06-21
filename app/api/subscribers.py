import secrets

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.subscriber import Subscriber
from app.schemas.subscriber import SubscriberCreate, SubscriberOut

router = APIRouter(prefix="/subscribers", tags=["subscribers"])


@router.post("/", response_model=SubscriberOut)
def create_subscriber(subscriber: SubscriberCreate, db: Session = Depends(get_db)):
    db_subscriber = Subscriber(
        target_url=subscriber.target_url,
        secret_key=secrets.token_hex(32),
    )
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber


@router.get("/", response_model=list[SubscriberOut])
def list_subscribers(db: Session = Depends(get_db)):
    return db.query(Subscriber).all()
