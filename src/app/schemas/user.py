from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserLogin(BaseModel):
    email: EmailStr = None
    password: str = None


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: int
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None


class UserCreated(UserCreate):
    id: int
