from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "PeticoesBR API"
    ENV: str = "production"
    HOST: str = "0.0.0.0"
    PORT: int = 3001

    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    TENANT_MODE: str = "single"  # single | multi_db
    TENANT_HEADER: str = "X-Tenant"

    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/peticoes"

    CORS_ORIGINS: str = "*"

    FILE_STORAGE_DIR: str = "/app/storage"
    MAX_UPLOAD_MB: int = 20

    SENDGRID_API_KEY: str | None = None
    WHATSAPP_TOKEN: str | None = None
    LLM_PROVIDER: str = "mock"
    LLM_API_KEY: str | None = None

    BASE_URL: str = "http://localhost:3001"

    @property
    def allowed_origins(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return ["*"]
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"  # ignore unknown envs
settings = Settings()
