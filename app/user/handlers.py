from datetime import timedelta

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, security, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import templates
from app.auth.auth import get_current_user
from app.auth.security import create_access_token
from app.errors import CustomError
from app.session import get_db
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

from .schema import Token, UserCreate, UserMe, UserRead
from .service import UserService

user_router = APIRouter()


@user_router.post('/register', response_model=UserRead, summary='Регистрация пользователя')
async def register(user: UserCreate, session: AsyncSession = Depends(get_db)):
    user_service = UserService(session)
    try:
        return await user_service.add_user(user)
    except CustomError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)


@user_router.post('/login', response_model=Token, summary='Аутентификация пользователя')
async def login(
        response: Response,
        form_data: security.OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_db),
):
    user_service = UserService(session)
    user = await user_service.authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверные учетные данные.')

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)

    # Создаем cookie с ключом access_token
    response.set_cookie(key="access_token", value=access_token)

    return {'access_token': access_token, 'token_type': 'bearer'}


@user_router.get("/me", response_model=UserMe, summary="Получить информацию о текущем пользователе")
async def get_me(request: Request, access_token: str = Cookie(None), session: AsyncSession = Depends(get_db)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = await get_current_user(access_token, session)

    # Если клиент ожидает HTML, возвращаем HTML-шаблон
    if "text/html" in request.headers.get("accept"):
        return templates.TemplateResponse("me.html", {"request": request, "user": user})

    return user
