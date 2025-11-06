from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from .config import settings

# Fábrica padrão (single-tenant ou fallback do multi_db)
default_engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, poolclass=NullPool)
DefaultSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=default_engine)

def make_session_for_url(url: str):
    engine = create_engine(url, pool_pre_ping=True, poolclass=NullPool)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
