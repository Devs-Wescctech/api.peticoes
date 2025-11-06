from sqlalchemy import Column, String, TIMESTAMP, Text, text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from . import Base

class MessageTemplate(Base):
    __tablename__ = "message_templates"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    subject = Column(String(500))
    content = Column(Text, nullable=False)
    is_default = Column(Boolean, server_default=text("false"))
    thumbnail_url = Column(Text)
    usage_count = Column(Integer, server_default=text("0"))
    created_by = Column(String(255))
    created_date = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_date = Column(TIMESTAMP, server_default=text("NOW()"))
