from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.session import get_db
from app.settings import ALGORITHM, SECRET_KEY
from app.user import User, UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Неверные учетные данные.',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await UserService(session).get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user
