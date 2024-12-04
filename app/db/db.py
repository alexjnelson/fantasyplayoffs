from fastapi import HTTPException
from sqlmodel import create_engine, Session
from functools import wraps
from sqlalchemy.exc import IntegrityError

from config import settings


engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
