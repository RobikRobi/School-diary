from pydantic import BaseModel


class CreateSubject(BaseModel):
    
    name_subject: str


class UpdateSubject(BaseModel):
    
    new_name_subject: str
