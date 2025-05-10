# выставление оценки пользователю за урок
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from src.db import get_session
from src.models.LessonModel import Lesson
from src.models.MarkModel import Mark
from src.models.UserModel import User
from src.get_current_user import get_current_user
from src.enum.UserEnum import UserRole
from src.marks.marks_shema import MarkRead
from src.auth.auth_utilits import valid_access_token

app = APIRouter(prefix="/marks", tags=["Grade"])



# вебсокет для выставления оценок
@app.websocket("/ws/grade")
async def grade_user_via_ws(websocket: WebSocket,
    session: AsyncSession = Depends(get_session)
):
    token = websocket.headers.get("Authorization")
    if not token:
        print("Error")
    token = token[7:]
    user_id = await valid_access_token(token)
    user = await session.scalar(select(User).where(User.id == user_id))

    if not user:
        await websocket.send_json({
            "token":"Your token is not valid", 
            "status":426
        })
        await websocket.close()
    await websocket.accept()
    
    # Проверяем роль пользователя
    if user.role != UserRole.TEACHER:
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

            await websocket.send_json({"status": "success", "student_id": student_id, "value": value})

    except WebSocketDisconnect:
        print("WebSocket disconnected")

        await session.commit()


# получение оценок
@app.get("/", response_model=List[MarkRead])
async def get_marks(
    group_id: Optional[int] = Query(None),
    subject_id: Optional[int] = Query(None),
    student_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    query = select(Mark).join(Mark.lesson).join(Mark.student)

    if group_id:
        query = query.where(Lesson.group_id == group_id)
    if subject_id:
        query = query.where(Lesson.subject_id == subject_id)
    if student_id:
        query = query.where(Mark.student_id == student_id)

    result = await session.execute(query)
    return result.scalars().all()