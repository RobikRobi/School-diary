import datetime

from pydantic import BaseModel, EmailStr, field_validator


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
    dob: datetime.date


class ShowUserWithToken(BaseModel):
    
    name: str
    surname: str
    patronymic: str
    snils: int
    dob: datetime.date

    token: str


class UpdateUser(BaseModel):

    name: str | None
    surname: str | None
    patronymic: str | None
    email: EmailStr | None
    snils: int | None

    password: str | bytes | None
    
    @field_validator("password")
    def check_password(cls, v):
        if not v:
            return None
        if  len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v