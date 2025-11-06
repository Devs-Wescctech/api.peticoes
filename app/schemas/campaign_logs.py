from pydantic import BaseModel
from typing import Optional

class CampaignLogIn(BaseModel):
    campaign_id: str
    recipient_name: str
    recipient_contact: str
    status: str
    response_status: Optional[str] = None
    response_body: Optional[str] = None
    error_message: Optional[str] = None

class CampaignLogOut(BaseModel):
    id: str
    campaign_id: str
    status: str
    class Config:
        from_attributes = True
