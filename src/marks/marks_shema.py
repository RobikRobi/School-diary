from pydantic import BaseModel

class MarkRead(BaseModel):
    id: int
    value: int
    lesson_id: int
    student_id: int

    class Config:
        from_attributes = True