from sqlalchemy import Column, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import UUID
from . import Base

class CampaignLog(Base):
    __tablename__ = "campaign_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    campaign_id = Column(UUID(as_uuid=True), nullable=False)
    recipient_name = Column(String(255), nullable=False)
    recipient_contact = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    response_status = Column(String(10))
    response_body = Column(Text)
    error_message = Column(Text)
    sent_at = Column(TIMESTAMP, server_default=text("NOW()"))
    created_by = Column(String(255))
    created_date = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_date = Column(TIMESTAMP, server_default=text("NOW()"))
