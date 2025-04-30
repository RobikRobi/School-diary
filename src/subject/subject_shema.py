from pydantic import BaseModel


class CreateSubject(BaseModel):
    
    name_subject: str
