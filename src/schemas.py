from pydantic import BaseModel, EmailStr, Field

from src.database.models import Role


class ContactModel(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=20)
    email: EmailStr
    phone: str
    birthday: str
    description: str


class ContactResponse(BaseModel):
    id: int
    name: str = 'Name'
    surname: str = 'Surname'
    email: EmailStr
    phone: str = '0993334567'
    birthday: str
    description: str

    class Config:
        orm_mode = True


class ContactName(BaseModel):
    name: str = 'Name'


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int
    username: str = Field(min_length=5, max_length=30)
    email: EmailStr
    avatar: str
    role: Role

    class Config:
        orm_mode = True


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    confirmed: bool

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr