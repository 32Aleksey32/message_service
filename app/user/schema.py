from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    telegram_id: int


class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    telegram_id: int


class UserMe(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    telegram_id: int


class Token(BaseModel):
    access_token: str
    token_type: str
