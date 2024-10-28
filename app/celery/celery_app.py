from celery import Celery

from app.settings import REDIS_BROKER_URL

celery_app = Celery(
    "tasks",
    broker=REDIS_BROKER_URL,
    backend=REDIS_BROKER_URL,
)
