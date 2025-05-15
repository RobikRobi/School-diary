from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.get_current_user import get_current_user
from src.db import get_session, async_session

from src.models.UserModel import User
from src.models.ChatModel import Chat
from src.models.MessageModel import Message

from src.chat.WebsocetConnect import manager
from src.auth.auth_utilits import valid_access_token


# Создаем экземпляр маршрутизатора с префиксом /chat и тегом "Chat"
app = APIRouter(prefix='/chat', tags=['Chat'])


@app.get("/chats")
async def get_chats(user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    chats = await session.scalars(select(Chat).where((Chat.sender_id == user.id)| (Chat.recipient_id == user.id)))
    return chats.all()

@app.post("/chats/creat")
async def creat_chat(recipient_id:int, user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    chat = Chat(sender_id=user.id, recipient_id=user.id)
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    return chat

@app.get("/chat/{chat_id}")
async def get_chat(chat_id:int, user:User = Depends(get_current_user), session:AsyncSession =Depends(get_session)):
    chat = await session.scalar(select(Chat).where(Chat.id == chat_id, 
                                                   (Chat.sender_id == user.id) | (Chat.recipient_id == user.id))
                                                   .options(selectinload(Chat.messages)))
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@app.websocket("/ws/chat/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, 
                             chat_id: int,
                             session: AsyncSession = Depends(get_session)):

    token = websocket.headers.get("Authorization")
    if not token:
        print("Error")
    token = token[7:]
    user_id = await valid_access_token(token)
    user = await session.scalar(select(User).where(User.id == user_id))
    chat = await session.scalar(select(Chat).where(Chat.id == chat_id))
    if not chat:
        await websocket.close()
        return
    
    await manager.connect(websocket, chat_id, user.id)
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            message = Message(chat_id=chat.id, text=data)
            async with async_session() as connetion:
                connetion.add(message)
                await connetion.commit()
                await connetion.refresh(message)

            await manager.broadcast(
                {
                    "message_id": message.id,
                    "sender_id": user.id,
                    "message": message.text
                }, 
                chat_id
            )
    except WebSocketDisconnect:

        await manager.disconnect(websocket, chat_id)
        print(f"Client disconnected from chat {chat_id}")