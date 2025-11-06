from pydantic import BaseModel
from typing import Optional

class PetitionIn(BaseModel):
    title: str
    description: str
    banner_url: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = "#6366f1"
    share_text: Optional[str] = None
    goal: int
    status: Optional[str] = "rascunho"
    slug: Optional[str] = None
    collect_phone: Optional[bool] = False
    collect_city: Optional[bool] = True
    collect_state: Optional[bool] = False
    collect_cpf: Optional[bool] = False
    collect_comment: Optional[bool] = True

class PetitionOut(BaseModel):
    id: str
    title: str
    description: str
    banner_url: Optional[str]
    logo_url: Optional[str]
    primary_color: Optional[str]
    share_text: Optional[str]
    goal: int
    status: str
    slug: Optional[str]
    views_count: int
    shares_count: int
    class Config:
        from_attributes = True
