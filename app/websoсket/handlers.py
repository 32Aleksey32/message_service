import json

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Form,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
    responses,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app import templates
from app.auth.auth import get_current_user
from app.message.service import MessageService
from app.session import get_db
from app.user import UserService

from .manager import ConnectionManager
from .utils import notify_if_offline

manager = ConnectionManager()

websocket_router = APIRouter()


@websocket_router.api_route("/chat", methods=["GET", "POST"])
async def chat(
        request: Request,
        access_token: str = Cookie(None),
        receiver_name: str = Form(None),
        session: AsyncSession = Depends(get_db)
):
    user_service = UserService(session)
    user = await get_current_user(access_token, session)

    # Если метод POST, перенаправляем на GET после обработки
    if request.method == "POST":
        receiver = await user_service.get_user_by_username(receiver_name)
        if not receiver:
            raise HTTPException(status_code=404, detail="Пользователь с таким username не найден.")

        url = f"/chat?receiver_name={receiver.username}"
        return responses.RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    # Получаем receiver_name из параметров запроса
    receiver_name = request.query_params.get("receiver_name")
    if not receiver_name:
        return templates.TemplateResponse("select_receiver.html", {"request": request})

    # Если receiver_name найден, отображаем чат
    context = {"request": request, "sender_name": user.username, "receiver_name": receiver_name}
    return templates.TemplateResponse("chat.html", context)


@websocket_router.websocket("/ws/{receiver_name}")
async def websocket_endpoint(
        websocket: WebSocket,
        receiver_name: str,
        access_token: str = Cookie(None),
        session: AsyncSession = Depends(get_db)
):
    message_service = MessageService(session)
    user_service = UserService(session)
    sender = await get_current_user(access_token, session)
    receiver = await user_service.get_user_by_username(receiver_name)

    await manager.connect(websocket, sender.id, sender.username)
    try:
        while True:
            message = await websocket.receive_text()
            message_data = json.loads(message)
            content = message_data['message']
            await manager.send_personal_message(message, receiver.id)
            await message_service.add_message(sender.id, receiver.id, content)

            # Уведомляем пользователя в telegram если он не в сети
            await notify_if_offline(receiver.username, sender.username, receiver.telegram_id)

    except WebSocketDisconnect:
        await manager.disconnect(sender.id, sender.username)
