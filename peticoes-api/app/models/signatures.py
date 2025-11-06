from sqlalchemy import Column, String, TIMESTAMP, Text, text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, INET
from . import Base

class Signature(Base):
    __tablename__ = "signatures"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    petition_id = Column(UUID(as_uuid=True), ForeignKey("petitions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    city = Column(String(255))
    state = Column(String(50))
    cpf = Column(String(14))
    comment = Column(Text)
    ip_address = Column(INET)
    user_agent = Column(Text)
    created_by = Column(String(255))
    created_date = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_date = Column(TIMESTAMP, server_default=text("NOW()"))
