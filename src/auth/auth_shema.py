import datetime

from pydantic import BaseModel, EmailStr, field_validator


class LoginUser(BaseModel):
    
    email: EmailStr
    password: str   
    

class RegisterUser(BaseModel):
        
    surname: str
    name: str
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
    

class UserShema(BaseModel):
    
    id: int
    surname: str
    name: str
    patronymic: str
    email: EmailStr
    snils: int
    dob: datetime.date


class ShowUserWithToken(BaseModel):
    
    surname: str
    name: str
    patronymic: str
    snils: int
    dob: datetime.date

    token: str


class UpdateUser(BaseModel):

    surname: str | None
    name: str | None
    patronymic: str | None
    email: EmailStr | None
    snils: int | None
    dob: datetime.date

    password: str | bytes | None
    
    @field_validator("password")
    def check_password(cls, v):
        if not v:
            return None
        if  len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v