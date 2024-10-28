from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .model import Message
from .repository import MessageRepository


class MessageService:
    def __init__(self, session: AsyncSession):
        self.repo = MessageRepository(session)

    async def add_message(self, sender_id: UUID, receiver_id: UUID, content) -> Message:
        new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
        await self.repo.add_message(new_message)
        return new_message

    async def get_messages_between_users(self, sender_id: UUID, receiver_id: UUID):
        return await self.repo.get_messages_between_users(sender_id, receiver_id)
