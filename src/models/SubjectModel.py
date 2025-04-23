import datetime
import typing

from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship

if typing.TYPE_CHECKING:
    from src.models.MarkModel import Lesson

from src.db import Base

class Subject(Base):
    __tablename__ = "subject_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name_subject: Mapped[str]
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="subject")