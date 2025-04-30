
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession



from src.db import get_session
from src.models.UserModel import User
from src.models.GroupModel import Group
from src.group.group_shema import CreateGroup

app = APIRouter(prefix="/group", tags=["group"])

@app.get("/groups")
async def get_groups(session:AsyncSession = Depends(get_session)):
    profiles = await session.scalars(select(Group))
    return profiles.all()

@app.get("/groups/{group_id}")
async def get_group(group_id:int, session:AsyncSession = Depends(get_session)):
    groups = await session.scalar(select(Group).where(Group.id == group_id).options(selectinload(Group.name)))
    return groups


@app.post("/subjects/create")
async def create_group(data:CreateGroup, session:AsyncSession = Depends(get_session)):
    newGroup = Group(**data.model_dump())
    session.add(newGroup)
    await session.commit()
    await session.refresh(newGroup)
    
    return newGroup