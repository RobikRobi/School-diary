import datetime

from pydantic import BaseModel


class DataLesson(BaseModel):

    subject_id: int | None
    teacher_id: int | None
    group_id: int | None

    date: datetime.datetime | None
    theme: str | None