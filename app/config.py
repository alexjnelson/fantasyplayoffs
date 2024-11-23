from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    DATABASE_URL: str = ""
    ALLOW_ORIGINS: list[str] = []    

    CLIENT_ID: str = ""
    CLIENT_SECRET: str = ""
    REDIRECT_URI: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
