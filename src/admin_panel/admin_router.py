from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.models.UserModel import User
from src.admin_panel.admin_shema import UpdateUserRole


app = APIRouter(prefix="/admin", tags=["admin"])


@app.put("/change-role")
async def change_user_role(
    data: UpdateUserRole,
    session: AsyncSession = Depends(get_session)
):
    # Найти пользователя
    result = await session.execute(select(User).where(User.id == data.user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Обновить роль
    user.role = data.new_role
    await session.commit()

    return {"message": "Роль пользователя успешно обновлена", "user_id": user.id, "new_role": user.role}