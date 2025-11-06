from pydantic import BaseModel
from typing import Optional

class MessageTemplateIn(BaseModel):
    name: str
    type: str
    subject: Optional[str] = None
    content: str
    is_default: Optional[bool] = False
    thumbnail_url: Optional[str] = None

class MessageTemplateOut(BaseModel):
    id: str
    name: str
    type: str
    is_default: bool
    class Config:
        from_attributes = True
