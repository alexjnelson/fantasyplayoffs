from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    DATABASE_URL: str = ""
    ALLOW_ORIGINS: List[str] = []

    # not necessary for dev environment
    CLIENT_ID: str = ""
    CLIENT_SECRET: str = ""
    REDIRECT_URI: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
