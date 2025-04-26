import datetime
from pydantic import BaseModel, EmailStr, field_validator
from src.enum.UserEnum import UserRole

class LoginUser(BaseModel):
    
    email: EmailStr
    password: str   
    
class RegisterUser(BaseModel):
        
    name: str
    surname: str
    patronymic: str
    snils: int

    login: str
    password: str | bytes 
    email: EmailStr
    role: UserRole
    dob: datetime.date
    
    @field_validator("password")
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v

class ShowUser(BaseModel):
    
    id: int
    name: str
    surname: str
    patronymic: str
    snils: int
    role: UserRole
    dob: datetime.date


class ShowUserWithToken(BaseModel):
    

    name: str
    surname: str
    patronymic: str
    snils: int
    role: UserRole
    dob: datetime.date

    token: str

class UpdateUser(BaseModel):

    name: str | None
    surname: str | None
    patronymic: str | None
    email: EmailStr | None
    snils: int | None
    role: UserRole | None

    password: str | bytes | None
    
    @field_validator("password")
    def check_password(cls, v):
        if not v:
            return None
        if  len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v