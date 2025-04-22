import datetime
import typing

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.db import Base

if typing.TYPE_CHECKING:
    from src.models.UserModel import User
    from src.models.SubjectModel import Subject

class Mark(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    
    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject_table.id"))

    student: Mapped["User"] = relationship(back_populates="marks", uselist=False)
    subject: Mapped["Subject"] = relationship(back_populates="marks", uselist=False)