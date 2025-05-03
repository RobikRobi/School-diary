from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.models.UserModel import User, UsersGroups
from src.models.GroupModel import Group
from src.group.group_shema import CreateGroup, AddUserToGroupSchema, GroupSchema
from src.auth.auth_shema import UserShema


app = APIRouter(prefix="/group", tags=["group"])

# получение списка всех групп
@app.get("/groups")
async def get_groups(session:AsyncSession = Depends(get_session)):
    profiles = await session.scalars(select(Group))
    return profiles.all()


@app.get("/groups/{group_id}", response_model=GroupSchema)
async def get_group_by_id(group_id: int, session: AsyncSession = Depends(get_session)):
    group = await session.scalar(select(Group).where(Group.id == group_id))

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return group

#создание группы
@app.post("/groups/create")
async def create_group(data:CreateGroup, session:AsyncSession = Depends(get_session)):
    newGroup = Group(**data.model_dump())
    session.add(newGroup)
    await session.commit()
    await session.refresh(newGroup)
    
    return newGroup

@app.post("/groups/users/add-user")
async def add_user_to_group(data: AddUserToGroupSchema, session: AsyncSession = Depends(get_session)):
    # Проверка существования пользователя и группы
    user = await session.scalar(select(User).where(User.id == data.user_id))
    group = await session.scalar(select(Group).where(Group.id == data.group_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Проверка, не добавлен ли уже
    check = await session.scalar(
        select(UsersGroups).where(
            UsersGroups.user_id == data.user_id,
            UsersGroups.group_id == data.group_id
        )
    )
    if check:
        raise HTTPException(status_code=400, detail="User already in group")

    # Добавление в таблицу связей
    stmt = insert(UsersGroups).values(user_id=data.user_id, group_id=data.group_id)
    await session.execute(stmt)
    await session.commit()

    return {"message": "User added to group"}

@app.get("/groups/users/{group_id}", response_model=list[UserShema])
async def get_users_in_group(group_id: int, session: AsyncSession = Depends(get_session)):
    group = await session.scalar(select(Group).where(Group.id == group_id).options(
        selectinload(Group.users)
    ))

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return group.users