from typing import List

from fastapi import APIRouter, Cookie, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import get_current_user
from app.errors import CustomError
from app.session import get_db
from app.user import UserService

from .schema import MessageHistory
from .service import MessageService

message_router = APIRouter()


@message_router.get("/{receiver_name}", response_model=List[MessageHistory], summary='Получить историю сообщений')
async def get_message_history(
        receiver_name: str,
        access_token: str = Cookie(None),
        session: AsyncSession = Depends(get_db)
):
    message_service = MessageService(session)
    user_service = UserService(session)
    try:
        sender = await get_current_user(access_token, session)
        receiver = await user_service.get_user_by_username(receiver_name)
        messages = await message_service.get_messages_between_users(sender.id, receiver.id)
        return MessageHistory.from_message(messages)
    except CustomError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)
