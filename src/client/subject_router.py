from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.subject_shema import SubjectAdd, SubjectDelete, SubjectRead, SubjectUpdate
from src.db import get_session
from src.models.SubjectModel import Subject


subject_router = APIRouter()


@subject_router.post("/subject/add")
async def subject_add(new_subject: SubjectAdd, session: AsyncSession = Depends(get_session)):

    Subject = Subject(**new_subject.model_dump())

    session.add(Subject)
    await session.commit()
    await session.refresh()

    return Subject


@subject_router.delete("/subject/delete")
async def subject_delete(subject: SubjectDelete, session: AsyncSession = Depends(get_session)):

    Subject = session.scalar(select(Subject).where(Subject.id == subject.subject_id))

    session.delete(Subject)
    await session.commit()
    await session.refresh

    return {"Subject delete"}


@subject_router.get("/subject/read")
async def subjeck_read(subject: SubjectRead, session: AsyncSession = Depends(get_session)):

    Subject = session.scalar(select(Subject).where(Subject.id == subject.subject_id))

    return Subject


@subject_router.put("/subject/update")
async def sublect_update(subject: SubjectUpdate, session: AsyncSession = Depends(get_session)):

    Subject = session.scalar(select(Subject).where(Subject.id == subject.subject_id))

    return Subject

    if Subject.subject_name:
        await Subject.sub