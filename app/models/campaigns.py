from sqlalchemy import Column, String, TIMESTAMP, Text, text, Integer, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from . import Base

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(50), server_default=text("'rascunho'"))
    petition_id = Column(UUID(as_uuid=True))
    target_petitions = Column(JSON)  # TEXT[] no SQL; aqui simplificado como JSON list
    target_filters = Column(JSON, server_default=text("'{}'"))
    message = Column(Text, nullable=False)
    subject = Column(String(500))
    sender_email = Column(String(255))
    sender_name = Column(String(255))
    scheduled_date = Column(TIMESTAMP)
    sent_count = Column(Integer, server_default=text("0"))
    success_count = Column(Integer, server_default=text("0"))
    failed_count = Column(Integer, server_default=text("0"))
    total_recipients = Column(Integer, server_default=text("0"))
    api_token = Column(Text)
    delay_seconds = Column(Integer, server_default=text("3"))
    messages_per_hour = Column(Integer, server_default=text("20"))
    avoid_night_hours = Column(Boolean, server_default=text("true"))
    started_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)
    created_by = Column(String(255))
    created_date = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_date = Column(TIMESTAMP, server_default=text("NOW()"))
