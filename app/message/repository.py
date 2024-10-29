from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from .model import Message


class MessageRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def add_message(self, message: Message) -> None:
        self.session.add(message)
        await self.session.commit()

    async def get_messages_between_users(self, sender_id: UUID, receiver_id: UUID):
        query = select(Message).options(
            joinedload(Message.sender),
            joinedload(Message.receiver)
        ).filter(
            ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) |
            ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
        )
        result = await self.session.execute(query)
        return result.scalars().all()
