from pydantic import BaseModel
from typing import Optional, List

class LinkBioPageIn(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    background_color: Optional[str] = "#6366f1"
    status: Optional[str] = "rascunho"
    petition_ids: Optional[list] = None

class LinkBioPageOut(BaseModel):
    id: str
    title: str
    slug: str
    status: str
    class Config:
        from_attributes = True
