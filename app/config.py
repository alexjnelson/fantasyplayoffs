from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"  # Replace with your DB URL
    CLIENT_ID = str = ""
    CLIENT_SECRET = str = ""
    REDIRECT_URI = str = ""

    class Config:
        env_file = ".env"

settings = Settings()
