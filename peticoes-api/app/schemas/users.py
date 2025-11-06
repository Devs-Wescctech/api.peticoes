from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "user"

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
