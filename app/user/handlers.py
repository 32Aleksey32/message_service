from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, responses, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import templates
from app.auth import get_current_user
from app.errors import CustomError
from app.services.redis_service import redis_create_session, redis_delete_session
from app.session import get_db

from .schema import LoginRequest, LoginResponse, UserCreate, UserRead
from .service import UserService

user_router = APIRouter()


@user_router.post('/register', response_model=UserRead, summary='Регистрация пользователя')
async def register(user: UserCreate, db_session: AsyncSession = Depends(get_db)):
    user_service = UserService(db_session)
    try:
        return await user_service.add_user(user)
    except CustomError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)


@user_router.post('/login', response_model=LoginResponse, summary='Аутентификация пользователя')
async def login(
        response: Response,
        request: LoginRequest,
        db_session: AsyncSession = Depends(get_db),
):
    user_service = UserService(db_session)
    user = await user_service.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверные учетные данные.')

    # Создаем сессию в redis
    session_id = await redis_create_session(user.id)

    # Создаем cookie с ключом session_id
    response.set_cookie(key="session_id", value=session_id)

    return LoginResponse(success=True, session_id=session_id, user=UserRead.from_user(user))


@user_router.post("/logout", summary="Выход из системы")
async def logout(request: Request, response: Response, session_id: str = Cookie(None)):
    if session_id:
        await redis_delete_session(session_id)
        response.delete_cookie("session_id")

        # Если клиент ожидает HTML, возвращаем HTML-шаблон
    if "text/html" in request.headers.get("accept"):
        return responses.RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    return {"message": "Вы вышли из системы"}


@user_router.get("/me", response_model=UserRead, summary="Получить информацию о текущем пользователе")
async def get_me(request: Request, session_id: str = Cookie(None), db_session: AsyncSession = Depends(get_db)):
    user = await get_current_user(session_id, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Если клиент ожидает HTML, возвращаем HTML-шаблон
    if "text/html" in request.headers.get("accept"):
        return templates.TemplateResponse("me.html", {"request": request, "user": user})

    return user
