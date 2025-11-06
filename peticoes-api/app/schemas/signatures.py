from pydantic import BaseModel, EmailStr
from typing import Optional

class SignatureIn(BaseModel):
    petition_id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    cpf: Optional[str] = None
    comment: Optional[str] = None

class SignatureOut(BaseModel):
    id: str
    petition_id: str
    name: str
    email: EmailStr
    city: Optional[str] = None
    state: Optional[str] = None
    comment: Optional[str] = None
    class Config:
        from_attributes = True
