from sqlalchemy import Column, String, Boolean, TIMESTAMP, text, JSON
from sqlalchemy.dialects.postgresql import UUID
from . import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), server_default=text("'user'"))
    phone = Column(String(50))
    avatar_url = Column(String)
    preferences = Column(JSON, server_default=text("'{ "email_notifications": true, "weekly_report": true }'"))
    email_verified = Column(Boolean, server_default=text("false"))
    reset_token = Column(String(255))
    reset_token_expires = Column(TIMESTAMP)
    created_date = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_date = Column(TIMESTAMP, server_default=text("NOW()"))
