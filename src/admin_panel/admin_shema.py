from pydantic import BaseModel
from src.enum.UserEnum import UserRole

class UpdateUserRole(BaseModel):
    user_id: int
    new_role: UserRole