from app.services.celery_tasks import send_telegram_notification
from app.services.redis_service import redis_get_status


async def notify_if_offline(receiver_username: str, sender_username: str, telegram_id: int):
    """
    Функция проверяет статус пользователя, если он отсутствует, то отправляет сообщение в telegram
    """
    message = f"Вам пришло сообщение от пользователя {sender_username}"
    redis_status = await redis_get_status(receiver_username)
    if not redis_status:
        await send_telegram_notification(telegram_id, message)
