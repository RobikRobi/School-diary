import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship
from sqlalchemy.sql import func

from typing import TYPE_CHECKING

from src.db import Base

class Subject(Base):
    __tablename__ = "subject_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name_subject:Mapped[str] = mapped_column(unique=True)

    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())