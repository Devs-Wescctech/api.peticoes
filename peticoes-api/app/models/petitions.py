from sqlalchemy import Column, String, Boolean, TIMESTAMP, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID
from . import Base

class Petition(Base):
    __tablename__ = "petitions"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    banner_url = Column(Text)
    logo_url = Column(Text)
    primary_color = Column(String(7), server_default=text("'#6366f1'"))
    share_text = Column(Text)
    goal = Column(Integer, nullable=False)
    status = Column(String(50), server_default=text("'rascunho'"))
    slug = Column(String(255), unique=True)
    collect_phone = Column(Boolean, server_default=text("false"))
    collect_city = Column(Boolean, server_default=text("true"))
    collect_state = Column(Boolean, server_default=text("false"))
    collect_cpf = Column(Boolean, server_default=text("false"))
    collect_comment = Column(Boolean, server_default=text("true"))
    views_count = Column(Integer, server_default=text("0"))
    shares_count = Column(Integer, server_default=text("0"))
    created_by = Column(String(255))
    created_date = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_date = Column(TIMESTAMP, server_default=text("NOW()"))
