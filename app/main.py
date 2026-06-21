from fastapi import FastAPI

from app.api import events, subscribers

app = FastAPI(title="Webhook Delivery Platform")

app.include_router(events.router)
app.include_router(subscribers.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
