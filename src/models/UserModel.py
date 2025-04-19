import datetime

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

    login:Mapped[str] = mapped_column(unique=True)
    password:Mapped[bytes]
    email:Mapped[str] = mapped_column(unique=True)

    dob:Mapped[datetime.date]

#    role:Mapped[str]

    marks:Mapped[list["Mark"]] = relationship(back_populates="student", uselist=True)
