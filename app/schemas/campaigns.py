from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CampaignIn(BaseModel):
    name: str
    type: str
    status: Optional[str] = "rascunho"
    petition_id: Optional[str] = None
    target_petitions: Optional[list] = None
    target_filters: Optional[Dict[str, Any]] = None
    message: str
    subject: Optional[str] = None
    sender_email: Optional[str] = None
    sender_name: Optional[str] = None
    scheduled_date: Optional[str] = None
    api_token: Optional[str] = None
    delay_seconds: Optional[int] = 3
    messages_per_hour: Optional[int] = 20
    avoid_night_hours: Optional[bool] = True

class CampaignOut(BaseModel):
    id: str
    name: str
    type: str
    status: str
    class Config:
        from_attributes = True
