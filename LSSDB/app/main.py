from fastapi import FastAPI, Depends, HTTPException
from app.database import engine, Base
from app.models import User
from sqlalchemy.orm import Session
from app.database import get_db

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI service is running!"}

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by ID from the database.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}