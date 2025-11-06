from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: str, expires_minutes: int | None = None):
    if expires_minutes is None:
        expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "exp": int(expire.timestamp())}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
