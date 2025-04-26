import datetime
import typing

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey


if typing.TYPE_CHECKING:
    from src.models.SubjectModel import Subject
    from src.models.UserModel import User
    from src.models.LessonModel import Lesson

from src.db import Base


class Group(Base):
    __tablename__ = "group_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name_group: Mapped[str]

    # Связи
    subjects: Mapped[list["Subject"]] = relationship(secondary="groupsubject", back_populates="groups", uselist=True)
    users: Mapped[list["User"]] = relationship(secondary="groupsubject", back_populates="groups", uselist=True)
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="group", uselist=True)


class GroupsSubjects(Base):
	__tablename__ = "groupsubject"
	group_id:Mapped[int] = mapped_column(ForeignKey("subject_table.id"),primary_key=True)
	subject_id:Mapped[int] = mapped_column(ForeignKey("group_table.id"),primary_key=True)