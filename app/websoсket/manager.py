from typing import Dict
from uuid import UUID

from fastapi import WebSocket

from app.services.redis_service import redis_create_status, redis_delete_status


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: UUID, username: str):
        await redis_create_status(username)
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: UUID, username: str):
        await redis_delete_status(username)
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, receiver_id: UUID):
        websocket = self.active_connections.get(receiver_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)
