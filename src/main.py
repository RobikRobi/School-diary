from binascii import Error
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import engine,Base


# from src.admin_panel.admin_router import app as admin_app

from src.models.UserModel import User
from src.models.SubjectModel import Subject
from src.models.LessonModel import Lesson
from src.models.MarkModel import Mark
from src.models.GroupModel import Group
from src.models.UserModel import User


from src.auth.auth_router import app as auth_app
from src.subject.subject_router import app as subject_app
from src.group.group_router import app as group_app
from src.lesson.lesson_router import app as lessons_app
from src.admin_panel.admin_router import app as admin_app
from src.marks.marks_router import app as marks_app
from src.chat.chat_router import app as chat_app


app = FastAPI()

# routers
app.include_router(auth_app)
app.include_router(subject_app)
app.include_router(group_app)
app.include_router(lessons_app)
app.include_router(admin_app)
app.include_router(marks_app)
app.include_router(chat_app)

# CORS

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

