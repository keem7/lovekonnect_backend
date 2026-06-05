from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


class UserBase(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    gender: str
    date_of_birth: date


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    profile_photo: Optional[str] = None
    interests: Optional[str] = None


class UserResponse(UserBase):
    id: int
    bio: Optional[str] = None
    location: Optional[str] = None
    profile_photo: Optional[str] = None
    interests: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True