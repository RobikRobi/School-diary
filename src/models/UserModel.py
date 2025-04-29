import datetime
import typing

from sqlalchemy import DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

if typing.TYPE_CHECKING:
    from src.models.MarkModel import Mark
    from src.models.GroupModel import Group
    from src.models.LessonModel import Lesson

from src.db import Base
from src.enum.UserEnum import UserRole

class User(Base):
    __tablename__ = "user_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]
    surname:Mapped[str]
    patronymic:Mapped[str]
    snils:Mapped[int] = mapped_column(unique=True)

    login:Mapped[str] = mapped_column(unique=True)
    password:Mapped[bytes]
    email:Mapped[str] = mapped_column(unique=True)
    role:Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.STUDENT)
    dob:Mapped[datetime.date]

    # связи
    marks: Mapped[list["Mark"]] = relationship(back_populates="student", uselist=True)
    groups: Mapped[list["Group"]] = relationship(secondary="usergroup", back_populates="users", uselist=True)
    lessons_taught: Mapped[list["Lesson"]] = relationship(back_populates="teacher", foreign_keys="Lesson.teacher_id")

    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class UsersGroups(Base):
    __tablename__ = "usergroup"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"),primary_key=True)
    group_id:Mapped[int] = mapped_column(ForeignKey("group_table.id"),primary_key=True)