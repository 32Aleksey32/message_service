from typing import List

from fastapi import APIRouter, Cookie, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.errors import CustomError
from app.services.redis_service import redis_get_cache, redis_set_cache
from app.session import get_db
from app.user import UserService

from .schema import MessageHistory
from .service import MessageService

message_router = APIRouter()


@message_router.get("/{receiver_name}", response_model=List[MessageHistory], summary='Получить историю сообщений')
async def get_message_history(
        receiver_name: str,
        session_id: str = Cookie(None),
        db_session: AsyncSession = Depends(get_db)
):
    message_service = MessageService(db_session)
    user_service = UserService(db_session)
    try:
        sender = await get_current_user(session_id, db_session)
        receiver = await user_service.get_user_by_username(receiver_name)

        cache_key = f"messages:{sender.id}:{receiver.id}"

        # Получаем и возвращаем закэшированные данные если они есть
        cached_messages = await redis_get_cache(cache_key)
        if cached_messages:
            return cached_messages

        messages = await message_service.get_messages_between_users(sender.id, receiver.id)
        messages_history = MessageHistory.from_message(messages)

        # Кэшируем полученные данные
        await redis_set_cache(key=cache_key, data=[msg.dict() for msg in messages_history])

        return messages_history
    except CustomError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)
