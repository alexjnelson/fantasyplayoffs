from sqlmodel import Session, select

from app.models import User
from app.db import handle_add_errors


@handle_add_errors
def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> User:
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()
    return user

def get_user_by_email(db: Session, email: str) -> User:
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    return user


def get_or_create_user(db: Session, new_user: User):
    user = get_user(db, User.id)
    if user is None:
        user = create_user(new_user)
    return user
