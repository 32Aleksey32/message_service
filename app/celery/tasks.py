from app.telegram_bot import bot

from .celery_app import celery_app


@celery_app.task
async def send_telegram_notification(telegram_id: int, message: str):
    await bot.send_message(chat_id=telegram_id, text=message)
