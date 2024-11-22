from pydantic import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    load_dotenv()

    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI: str = os.getenv("REDIRECT_URI")

    class Config:
        env_file = ".env"

settings = Settings()
