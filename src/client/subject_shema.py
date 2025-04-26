from pydantic import BaseModel


class SubjectAdd(BaseModel):

    name_subject: str


class SubjectDelete(BaseModel):

    subject_id: int


class SubjectRead(BaseModel):

    subject_id: int


class SubjectUpdate(BaseModel):

    subject_id: int

    subject_name: str
