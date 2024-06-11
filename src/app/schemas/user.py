from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserLogin(BaseModel):
    email: EmailStr = None
    password: str = None


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: PhoneNumber
    password: str = Field(..., min_length=6)


class ShowUser(BaseModel):
    id: int
    email: EmailStr
    phone_number: PhoneNumber
    is_active: bool

    class Config:
        orm_mode = True
