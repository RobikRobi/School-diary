from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.get_current_user import get_current_user
from src.db import get_session

from src.models.UserModel import User
from src.models.ChatModel import Chat, Message

from src.chat.WebsocetConnect import manager