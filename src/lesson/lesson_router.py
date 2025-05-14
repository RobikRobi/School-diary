from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.lesson.lesson_shema import DataLesson
from src.db import get_session
from src.models.LessonModel import Lesson


app = APIRouter(prefix="/lesson", tags=["Lessons"])


@app.post("/lesson/create")
async def create_lesson(lesson:DataLesson, session:AsyncSession = Depends(get_session)):

    NewLesson = Lesson(**lesson.model_dump())

    session.add(NewLesson)
    await session.commit()
    await session.refresh(NewLesson)

    return NewLesson


@app.get("/lesson/get")
async def get_lessons_group(group_id:int, session:AsyncSession = Depends(get_session)):

    lessons = await session.scalars(select(Lesson).where(Lesson.group_id == group_id))

    return lessons.all()


@app.delete("/lesson/delete")
async def delete_lesson(lesson_id:int, session:AsyncSession = Depends(get_session)):

    lesson = await session.scalar(select(Lesson).where(Lesson.id == lesson_id))

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    await session.delete(lesson)
    await session.commit()
    
    return {"lesson delete"}


@app.put("/lesson/update")
async def update_lesson(lesson_id:int, data_lesson:DataLesson, session:AsyncSession = Depends(get_session)):

    lesson = await session.scalar(select(Lesson).where(Lesson.id == lesson_id))

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if data_lesson.subject_id:
        lesson.subject_id = data_lesson.subject_id
    if data_lesson.teacher_id:
        lesson.teacher_id = data_lesson.teacher_id
    if data_lesson.group_id:
        lesson.group_id = data_lesson.group_id
    if data_lesson.date:
        lesson.date = data_lesson.date
    if data_lesson.theme:
        lesson.theme = data_lesson.theme

    await session.commit()
    await session.refresh(lesson)

    return lesson