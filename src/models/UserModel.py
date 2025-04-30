import datetime
import typing

from sqlalchemy import DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

if typing.TYPE_CHECKING:
    from src.models.MarkModel import Mark
    from src.models.LessonModel import Lesson
    from src.models.SubjectModel import Subject

from src.db import Base
from src.enum.UserEnum import UserRole

class User(Base):
    __tablename__ = "user_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    lesson_id: Mapped[int] = mapped_column(ForeignKey('lesson_table.id'))

    name:Mapped[str]
    surname:Mapped[str]
    patronymic:Mapped[str]
    snils:Mapped[int] = mapped_column(unique=True)

    login:Mapped[str] = mapped_column(unique=True)
    password:Mapped[bytes]
    email:Mapped[str] = mapped_column(unique=True)
    user_role:Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.STUDENT)
    dob:Mapped[datetime.date]
    role:Mapped[UserRole]

    # связи 
    marks: Mapped[list["Mark"]] = relationship(back_populates="student", uselist=True)
    lessons_taught: Mapped[list["Lesson"]] = relationship(back_populates="teacher", foreign_keys="lesson_table.teacher_id")

    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    dob:Mapped[datetime.date]

    marks:Mapped[list["Mark"]] = relationship(back_populates="student", uselist=True)
    subjects: Mapped[list["Subject"]] = relationship(secondary="usersubject", back_populates="users", uselist=True)


class UserSubject(Base):
	__tablename__ = "user_subject"
     
	user_id:Mapped[int] = mapped_column(ForeignKey('user_table.id'), primary_key=True)
	subject_id:Mapped[int] = mapped_column(ForeignKey('subject_table.id'), primary_key=True)
