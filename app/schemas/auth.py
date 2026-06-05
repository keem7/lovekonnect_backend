from pydantic import BaseModel, EmailStr
from datetime import date


class RegisterRequest(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    gender: str
    date_of_birth: date


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"