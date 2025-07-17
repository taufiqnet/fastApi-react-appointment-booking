from celery import Celery
from app.core.config import settings

celery = Celery(
    "appointment_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery.conf.timezone = "UTC"
