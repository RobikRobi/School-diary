from pydantic import BaseModel


class CreateGroup(BaseModel):
    
    name_group: str
