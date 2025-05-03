from pydantic import BaseModel


class CreateGroup(BaseModel):
    name_group: str

class AddUserToGroupSchema(BaseModel):
    user_id: int
    group_id: int

class GroupSchema(BaseModel):
    id: int
    name_group: str

class GroupUpdateRequest(BaseModel):
    name_group: str

class AddSubjectToGroupRequest(BaseModel):
    subject_id: int