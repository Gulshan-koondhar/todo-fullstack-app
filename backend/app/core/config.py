from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database - Allow environment variable override for Hugging Face
    DATABASE_URL: str = "sqlite:///./todo.db"  # Default to SQLite for Hugging Face compatibility

    # JWT
    BETTER_AUTH_SECRET: str = "change-me-in-production"

    # CORS - Include Hugging Face Space URL pattern and allow environment override
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004,http://localhost:3005,http://localhost:3006,https://*.hf.space,https://*.huggingface.co"

    # Server - Use environment variables for Hugging Face
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 7860

    # Hugging Face Space info (auto-set by HF)
    HF_SPACE_ID: str = ""

    # AI Configuration
    OPENROUTER_API_KEY: str = ""
    AI_MODEL: str = "openai/gpt-3.5-turbo"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
