from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.models.UserModel import User
from src.models.SubjectModel import Subject
from src.subject.subject_shema import CreateSubject


subject_router = APIRouter(prefix="/subject", tags=["subject"])


@subject_router.get("/subjects")
async def get_subjects(session:AsyncSession = Depends(get_session)):

    profiles = await session.scalars(select(Subject))

    return profiles.all()


@subject_router.get("/subjects/{subject_id}")
async def get_subject(subject_id:int, session:AsyncSession = Depends(get_session)):

    subject = await session.scalar(select(Subject).where(Subject.id == subject_id).options(selectinload(Subject.name)))

    return subject


@subject_router.post("/subjects/create")
async def create_product(data:CreateSubject, session:AsyncSession = Depends(get_session)):

    newSubject = Subject(**data.model_dump())

    session.add(newSubject)
    await session.commit()
    await session.refresh(newSubject)

    return newSubject