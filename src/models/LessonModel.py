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
    from src.models.UserModel import User

from src.db import Base


class Lesson(Base):
    __tablename__ = "lesson_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    subject_id: Mapped[int] = mapped_column(ForeignKey("subject_table.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))

    date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    theme: Mapped[str] = mapped_column(nullable=True, default=None)

    # Связи
    subject: Mapped["Subject"] = relationship(back_populates="lessons")
    teacher: Mapped["User"] = relationship(back_populates="lessons_taught", foreign_keys=[teacher_id])
    marks: Mapped[list["Mark"]] = relationship(back_populates="lesson")
