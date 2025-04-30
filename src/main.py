from binascii import Error
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db import engine,Base
from src.auth.auth_router import app as auth_app
from src.client.subject_router import subject_router

# from src.admin_panel.admin_router import app as admin_app

from .models.UserModel import User
from .models.SubjectModel import Subject
from .models.LessonModel import Lesson
from .models.MarkModel import Mark


app = FastAPI()

# routers
app.include_router(auth_app)
app.include_router(subject_router)

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

@app.get("/init")
async def create_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except Error as e:
            print(e)     
        await  conn.run_sync(Base.metadata.create_all)
    return({"msg":"db creat! =)"})