from sqlalchemy import Column, String, TIMESTAMP, Text, text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from . import Base

class LinkBioPage(Base):
    __tablename__ = "linkbio_pages"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    avatar_url = Column(Text)
    background_color = Column(String(7), server_default=text("'#6366f1'"))
    status = Column(String(50), server_default=text("'rascunho'"))
    petition_ids = Column(Text)  # TEXT[] no SQL; simplificado aqui como string JSON
    views_count = Column(Integer, server_default=text("0"))
    clicks_count = Column(Integer, server_default=text("0"))
    created_by = Column(String(255))
    created_date = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_date = Column(TIMESTAMP, server_default=text("NOW()"))
