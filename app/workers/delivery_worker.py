import httpx

from app.workers.celery_app import celery_app
from app.database import SessionLocal
from app.models.event import Event
from app.models.subscriber import Subscriber
from app.models.delivery import Delivery


@celery_app.task(name="deliver_webhook")
def deliver_webhook(delivery_id: str):
    db = SessionLocal()
    try:
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if not delivery:
            return

        event = db.query(Event).filter(Event.id == delivery.event_id).first()
        subscriber = db.query(Subscriber).filter(Subscriber.id == delivery.subscriber_id).first()

        try:
            response = httpx.post(
                subscriber.target_url,
                json={"event_type": event.event_type, "payload": event.payload},
                timeout=5.0,
            )
            response.raise_for_status()
            delivery.status = "success"
        except Exception:
            delivery.status = "failed"
        finally:
            delivery.attempt_count += 1
            db.commit()
    finally:
        db.close()
