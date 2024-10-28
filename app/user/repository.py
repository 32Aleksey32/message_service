from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .model import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: User) -> None:
        self.session.add(user)
        await self.session.commit()

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> User:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_user_by_id(self, user_id: UUID) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def check_existing_user(self, email: str, username: str) -> User:
        query = select(User).where(or_(User.email == email, User.username == username))
        result = await self.session.execute(query)
        return result.scalars().first()
