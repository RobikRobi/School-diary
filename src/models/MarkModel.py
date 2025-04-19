from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.UserModel import User
#    from src.models.SubjectModel import Subject

class Mark(Base):

    id:Mapped[int] = mapped_column(primary_key=True)

    mark:Mapped[int]

    student_id:Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete="CASCADE"), primary_key=True)
    student:Mapped["User"] = relationship(back_populates="user_table", uselist=False)
#    subject_id:Mapped[int] = mapped_column(ForeignKey("subject_table.id", ondelete="CASCADE"), primary_key=True)
#    subject:Mapped["Subject"] = relationship(back_populates="")