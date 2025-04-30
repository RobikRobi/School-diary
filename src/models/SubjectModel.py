import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
    from src.models.MarkModel import Lesson
    from src.models.GroupModel import Group

from src.db import Base

class Subject(Base):
    __tablename__ = "subject_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name_subject: Mapped[str]
    groups: Mapped[list["Group"]] = relationship(secondary="groupsubject", back_populates="subjects", uselist=True)
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="subject")