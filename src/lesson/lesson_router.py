from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.lesson.lesson_shema import DataLesson
from src.db import get_session
from src.models.LessonModel import Lesson
from src.models.MarkModel import Mark
from src.models.UserModel import User
from src.get_current_user import get_current_user
from src.enum.UserEnum import UserRole


app = APIRouter(prefix="/lesson", tags=["lessons"])


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

    await session.delete(lesson)
    await session.commit()
    
    return {"lesson delete"}


@app.put("/lesson/update")
async def update_lesson(lesson_id:int, data_lesson:DataLesson, session:AsyncSession = Depends(get_session)):

    lesson = await session.scalar(select(Lesson).where(Lesson.id == lesson_id))

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

# выставление оценки пользователю за урок
@app.websocket("/ws/grade")
async def grade_user_via_ws(websocket: WebSocket,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    await websocket.accept()
    
    # Проверяем роль пользователя
    if current_user.role != UserRole.TEACHER:
        await websocket.send_json({"error": "Access denied. Only TEACHERs can assign marks."})
        await websocket.close()
        return

    try:
        while True:
            data = await websocket.receive_json()

            student_id = data.get("student_id")
            lesson_id = data.get("lesson_id")
            value = data.get("value")

            if not all([student_id, lesson_id, value]):
                await websocket.send_json({"error": "Missing fields"})
                continue

            # Проверим, есть ли уже оценка
            stmt = select(Mark).where(
                Mark.student_id == student_id,
                Mark.lesson_id == lesson_id
            )
            result = await session.execute(stmt)
            mark = result.scalars().first()

            if mark:
                mark.value = value  # обновим оценку
            else:
                mark = Mark(student_id=student_id, lesson_id=lesson_id, value=value)
                session.add(mark)

            await session.commit()

            await websocket.send_json({"status": "success", "student_id": student_id, "value": value})

    except WebSocketDisconnect:
        print("WebSocket disconnected")