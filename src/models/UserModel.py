import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship
from src.enum.UserEnum import UserRole
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship

from typing import TYPE_CHECKING

from src.db import Base

if TYPE_CHECKING:
    from src.models.MarkModel import Mark

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
