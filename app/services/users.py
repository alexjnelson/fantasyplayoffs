from sqlmodel import Session, select

from models import Users
from db import handle_add_errors


@handle_add_errors
def create_user(db: Session, user: Users) -> Users:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: str) -> Users:
    statement = select(Users).where(Users.id == user_id)
    user = db.exec(statement).first()
    return user

def get_user_by_email(db: Session, email: str) -> Users:
    statement = select(Users).where(Users.email == email)
    user = db.exec(statement).first()
    return user


def get_or_create_user(db: Session, new_user: Users):
    user = get_user(db, new_user.id)
    if user is None:
        user = create_user(db, new_user)
    return user
