from sqlmodel import create_engine, Session
from app.config import settings

# Create the database engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# Dependency to get a session
def get_session():
    with Session(engine) as session:
        yield session
