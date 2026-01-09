from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/todo"

    # JWT
    BETTER_AUTH_SECRET: str = "change-me-in-production"

    # CORS
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"

    # Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 7860

    # Hugging Face Space info (auto-set by HF)
    HF_SPACE_ID: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
