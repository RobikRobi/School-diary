import datetime
import typing

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship
from sqlalchemy.sql import func

if typing.TYPE_CHECKING:
    from src.models.UserModel import User
    from src.models.MarkModel import Mark

from src.db import Base

class Subject(Base):
    __tablename__ = "subject_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name_subject: Mapped[str] = mapped_column(unique=True)
    marks: Mapped[list["Mark"]] = relationship(back_populates="subject", uselist=True)
    users: Mapped[list["User"]] = relationship(secondary="usersubject", back_populates="subjects", uselist=True)

    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())