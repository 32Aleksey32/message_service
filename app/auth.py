from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.redis_service import redis_get_session
from app.session import get_db
from app.user import UserService


async def get_current_user(session_id: str = Cookie(None), db_session: AsyncSession = Depends(get_db)):
    if session_id is None:
        raise HTTPException(status_code=401, detail="Сессия не найдена")

    user_id = await redis_get_session(session_id)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Сессия истекла или недействительна")

    user = await UserService(db_session).get_user_by_id(user_id=user_id)
    return user
