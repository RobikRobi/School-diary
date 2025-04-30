import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.db import Base

if typing.TYPE_CHECKING:
    from src.models.UserModel import User
    from src.models.LessonModel import Lesson

class Mark(Base):
    __tablename__ = "mark_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson_table.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    value: Mapped[int]
    
    # Связи
    lesson: Mapped["Lesson"] = relationship(back_populates="marks")
    student: Mapped["User"] = relationship(back_populates="marks")