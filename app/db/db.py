from fastapi import HTTPException
from sqlmodel import create_engine, Session
from app.config import settings
from functools import wraps
from sqlalchemy.exc import IntegrityError


engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def handle_add_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            # Rollback the session if an IntegrityError occurs
            db = kwargs.get("db")
            if db:
                db.rollback()
            # Check for specific error types if needed
            raise HTTPException(status_code=400, detail=str(e.orig))
    return wrapper
