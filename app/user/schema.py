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

    @classmethod
    def from_user(cls, user):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            telegram_id=user.telegram_id
        )


class LoginResponse(BaseModel):
    success: bool
    session_id: str
    user: UserRead


class LoginRequest(BaseModel):
    username: str
    password: str
