from sqlmodel import Session, select
from app.models import User


def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def read_user(session: Session, user_id: int):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user
