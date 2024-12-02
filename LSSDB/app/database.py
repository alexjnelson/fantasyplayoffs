from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlmodel import create_engine, Session
from functools import wraps
from sqlalchemy.exc import IntegrityError

DATABASE_URL = "postgresql://postgres:mypassword@localhost:5432/mydatabase"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session


def handle_add_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            db = kwargs.get("db")
            if db:
                db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
    return wrapper