import logging
import asyncio
from fastapi import Body, FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlmodel import Session
from app.models import Users
from app.database import get_session
from app.config.logging_config import setup_logging
import random 


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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    try:
        while True:
            message = await websocket.receive_text()  # Receive a message
            print(f"Received: {message}")
            await websocket.send_text(f"Echo: {message}")  # Echo the message back
    except WebSocketDisconnect:
        print("Client disconnected")

@app.websocket("/ws/football")
async def football_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Generate mock live data
            mock_data = generate_mock_data()
            await websocket.send_json(mock_data)  # Send JSON data to the client
            await asyncio.sleep(5)  # Simulate delay between updates
    except WebSocketDisconnect:
        print("Client disconnected")

def generate_mock_data():
    # Mock live football data
    return {
        "game_id": "12345",
        "quarter": random.randint(1, 4),
        "time_remaining": f"{random.randint(0, 15)}:{random.randint(0, 59):02}",
        "team_a": {
            "name": "Eagles",
            "score": random.randint(0, 50),
            "possession": random.choice([True, False])
        },
        "team_b": {
            "name": "Patriots",
            "score": random.randint(0, 50),
            "possession": random.choice([True, False])
        },
        "last_play": random.choice(["Touchdown by Player 10", "Field Goal", "Fumble Recovery", "Interception"])
    }