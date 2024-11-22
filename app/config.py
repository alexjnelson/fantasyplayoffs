from pydantic import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"

    DATABASE_URL: str = None

    CLIENT_ID: str = None
    CLIENT_SECRET: str = None
    REDIRECT_URI: str = None

    class Config:
        env_file = ".env"

settings = Settings()
