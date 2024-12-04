from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlmodel import create_engine, Session
from functools import wraps
from sqlalchemy.exc import IntegrityError


# DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

DATABASE_URL = "postgresql://postgres:mypassword@localhost:5432/mydatabase"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
