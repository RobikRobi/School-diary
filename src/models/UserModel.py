import datetime
import typing

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship
from src.enum.UserEnum import UserRole
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship

if typing.TYPE_CHECKING:
    from src.models.SubjectModel import Subject
    from src.models.MarkModel import Mark

from src.db import Base


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
    user_role:Mapped[UserRole]

    dob:Mapped[datetime.date]
    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    dob:Mapped[datetime.date]

#    role:Mapped[str]

    marks:Mapped[list["Mark"]] = relationship(back_populates="student", uselist=True)
    subjects: Mapped[list["Subject"]] = relationship(secondary="usersubject", back_populates="users", uselist=True)


class UserSubject(Base):
	__tablename__ = "usersubject"
	user_id:Mapped[int] = mapped_column(ForeignKey('user.id'),primary_key=True)
	subject_id:Mapped[int] = mapped_column(ForeignKey('subject.id'),primary_key=True)