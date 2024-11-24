from fastapi import FastAPI, Depends, HTTPException
from app.models import Users
from sqlalchemy.orm import Session
from app.database import get_session
from sqlmodel import Session, text

# Initialize database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI service is running!"}

@app.get("/users/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_session)):
    """
    Retrieve a user by ID from the database.
    """
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}


@app.delete("/users/raw-delete/{user_id}")
def raw_delete_user(user_id: str, db: Session = Depends(get_session)):
    try:
        db.exec(text(f"DELETE FROM users WHERE id = {user_id}"))
        db.commit()
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    return {"message": "User deleted successfully"}


# def get_user(db: Session, user_id: str) -> Users:
#     statement = select(Users).where(Users.id == user_id)
#     user = db.exec(statement).first()
#     return user