from celery import Celery

from app.services.telegram_bot import bot
from app.settings import REDIS_URL

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)


@celery_app.task
async def send_telegram_notification(telegram_id: int, message: str):
    await bot.send_message(chat_id=telegram_id, text=message)
