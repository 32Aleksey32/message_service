from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.redis_service import redis_delete_cache

from .model import Message
from .repository import MessageRepository


class MessageService:
    def __init__(self, db_session: AsyncSession):
        self.repo = MessageRepository(db_session)

    async def add_message(self, sender_id: UUID, receiver_id: UUID, content) -> Message:
        new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
        await self.repo.add_message(new_message)

        # Удаляем старые кэшированные данные
        cache_key = f"messages:{sender_id}:{receiver_id}"
        await redis_delete_cache(cache_key)

        return new_message

    async def get_messages_between_users(self, sender_id: UUID, receiver_id: UUID):
        return await self.repo.get_messages_between_users(sender_id, receiver_id)
