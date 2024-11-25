import logging
from fastapi import Body, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import Session

from app.models import Users
from app.database import get_session
from app.config.logging_config import setup_logging


# Set up logging
setup_logging()
api_logger = logging.getLogger("api")
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI service is running!"}

@app.get("/users/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_session)):
    """
    Retrieve a user by ID from the database.
    """
    api_logger.info(f"Fetching user with ID: {user_id}")
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    api_logger.info(f"User retrieved: {user.name} ({user.email})")
    return {"id": user.id, "name": user.name, "email": user.email}


@app.delete("/users/delete/{user_id}")
def raw_delete_user(user_id: str, db: Session = Depends(get_session)):
    api_logger.info(f"Attempting to delete user with ID: {user_id}")
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        api_logger.warning(f"User with ID {user_id} not found for deletion")
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        db.delete(user)
        db.commit()
        api_logger.info(f"User with ID {user_id} successfully deleted")
    except Exception as e:
        db.rollback()
        api_logger.error(f"Failed to delete user with ID {user_id}: {e}")
        return {"error": str(e)}
    return {"message": "User deleted successfully"}


@app.post("/users/create")
async def create_user(email: str = Body(...), name: str = Body(...), db: Session = Depends(get_session)):
    api_logger.info(f"Creating user: {name} with email: {email}")
    user = Users(
        id=email,
        name=name,
        email=email
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        api_logger.info(f"User created successfully: {name} ({email})")
    except Exception as e:
        db.rollback()
        api_logger.error(f"Failed to create user {name} ({email}): {e}")
        return {"error": str(e)}
    
    return {
        "message": "User created successfully",
        "google_id": user.id,
    }



# def get_user(db: Session, user_id: str) -> Users:
#     statement = select(Users).where(Users.id == user_id)
#     user = db.exec(statement).first()
#     return user