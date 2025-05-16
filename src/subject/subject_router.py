from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.models.UserModel import User
from src.models.SubjectModel import Subject
from src.models.GroupModel import Group
from src.subject.subject_shema import CreateSubject, UpdateSubject


app = APIRouter(prefix="/subject", tags=["Subject"])

# получение всех предметов
@app.get("/subjects")
async def get_subjects(session:AsyncSession = Depends(get_session)):

    profiles = await session.scalars(select(Subject))

    return profiles.all()

# получение конкретного предмета
@app.get("/subjects/{subject_id}")
async def get_subject(subject_id: int, session: AsyncSession = Depends(get_session)):

    subject = await session.scalar(select(Subject).where(Subject.id == subject_id))

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject

# создание предмета
@app.post("/subjects/create")
async def create_subject(data:CreateSubject, session:AsyncSession = Depends(get_session)):

    newSubject = Subject(**data.model_dump())

    session.add(newSubject)
    await session.commit()
    await session.refresh(newSubject)

    return newSubject

# удаление предмета
@app.delete("/subjects/delete")
async def delete_subject(subject_id:int, session:AsyncSession = Depends(get_session)):

    subject = await session.scalar(select(Subject).where(Subject.id == subject_id))

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    await session.delete(subject)
    await session.commit()

    return {"Subject delete"}

# изменение предмета
@app.put("/subjects/update")
async def update_subject(subject_id:int, subject_data: UpdateSubject, session:AsyncSession = Depends(get_session)):
    
    subject = await session.scalar(select(Subject).where(Subject.id == subject_id))

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    if subject_data.new_name_subject:
        subject.name_subject = subject_data.new_name_subject

    await session.commit()
    await session.refresh(subject)

    return subject

# получение всех групп предмета
@app.get("/{subject_id}/groups")
async def get_groups_by_subject(subject_id: int, session: AsyncSession = Depends(get_session)):

    subject = await session.scalar(select(Subject).where(Subject.id == subject_id))
    
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    groups = await session.execute(select(Group).where(Group.subject_id == subject_id))
    group_list = groups.scalars().all()

    return [
        {
            "id": group.id,
            "name_group": group.name_group
        } for group in group_list
    ]

