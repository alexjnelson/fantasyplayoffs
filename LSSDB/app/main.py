from fastapi import Body, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import Session

from app.models import Users
from app.database import get_session

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
    print(db.query(Users).all())
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}


@app.delete("/users/delete/{user_id}")
def raw_delete_user(user_id: str, db: Session = Depends(get_session)):
    user = db.query(Users).filter(Users.id == user_id).first()
    
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    return {"message": "User deleted successfully"}


@app.post("/users/create")
async def create_user(email: str = Body(...), name: str = Body(...), db: Session = Depends(get_session)):
    user = Users(
        id=email,
        name=name,
        email=email
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
    return {
        "message": "User created successfully",
        "google_id": user.id,
    }



# def get_user(db: Session, user_id: str) -> Users:
#     statement = select(Users).where(Users.id == user_id)
#     user = db.exec(statement).first()
#     return user