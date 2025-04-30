from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from models.UserModel import User
from auth.auth_shema import UpdateUser, ShowUser
from get_current_user import get_current_user


app = APIRouter(prefix="/admin", tags=["admin"])


@app.put("/update", response_model=ShowUser)
async def update_user(data:UpdateUser,me:User = Depends(get_current_user) ,session:AsyncSession = Depends(get_session)):
    
    await session.refresh(me)
    if data.name:
        me.name = data.name
    if data.surname:
        me.surname = data.surname
    if data.patronymic:
        me.patronymic = data.patronymic
    if data.email:
        me.email = data.email
    if data.snils:
        me.snilas = data.snils
    if data.role:
        me.role = data.role

    await session.commit()
    await session.refresh(me)

    return me