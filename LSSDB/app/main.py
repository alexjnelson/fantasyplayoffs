import logging
import asyncio
from fastapi import Body, FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlmodel import Session
from app.models import Users
from app.database import get_session
from app.config.logging_config import setup_logging
from app.enums.live_update_command import LiveUpdateCommand
from app.utils.mock_data_generator import generate_mock_data


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

## WEBSOCKET ENDPOINTS ##
send_updates_event = asyncio.Event()  # Event to control live updates

@app.post("/start")
async def start_live_updates():
    """
    Start generating and sending live game data to WebSocket clients.
    """
    global stop_flag, update_task

    if stop_flag is False and update_task is not None:
        return {"message": "Live updates are already running."}

    stop_flag = False  # Allow updates to start
    update_task = asyncio.create_task(send_live_updates())  # Start background task
    api_logger.info("Live updates started.")
    return {"message": "Live updates started."}


@app.post("/stop")
async def stop_live_updates():
    """
    Stop generating and sending live game data.
    """
    global stop_flag, update_task

    if stop_flag is True or update_task is None:
        return {"message": "Live updates are already stopped."}

    stop_flag = True  # Stop updates
    if update_task:
        api_logger.info("Cancelling update task...")
        update_task.cancel()
        try:
            await update_task  # Wait for the task to finish
        except asyncio.CancelledError:
            api_logger.info("Update task cancelled.")

    update_task = None
    api_logger.info("Live updates stopped.")
    return {"message": "Live updates stopped."}


active_connections = []

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
async def live_data_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for live football updates.
    Responds to start/stop commands and sends live updates.
    """
    await websocket.accept()
    active_connections.append(websocket)
    api_logger.info(f"New WebSocket connection established: {websocket.client}")

    try:
        while True:
            # Wait for a command from the client
            command = await websocket.receive_text()
            api_logger.info(f"Received command: {command}")

            if command.lower() == LiveUpdateCommand.START:
                send_updates_event.set()  # Enable updates
                api_logger.info("Live updates started.")
                await websocket.send_text("Live updates started.")
                # Start sending updates in the background
                asyncio.create_task(send_live_updates(websocket))
            elif command.lower() == LiveUpdateCommand.STOP:
                send_updates_event.clear()  # Disable updates
                api_logger.info("Live updates stopped.")
                await websocket.send_text("Live updates stopped.")
            else:
                api_logger.warning(f"Unknown command received: {command}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        api_logger.warning(f"WebSocket client disconnected: {websocket.client}")
    except Exception as e:
        api_logger.error(f"Error in WebSocket connection with {websocket.client}: {e}")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)

async def send_live_updates(websocket: WebSocket):
    """
    Send live updates to a single WebSocket client while updates are enabled.
    """
    try:
        while send_updates_event.is_set():
            mock_data = generate_mock_data()
            await websocket.send_json(mock_data)
            api_logger.info(f"Sent live update: {mock_data}")
            await asyncio.sleep(5)  # Simulate delay between updates
    except Exception as e:
        api_logger.error(f"Failed to send live update: {e}")


@app.on_event("shutdown")
async def shutdown():
    """
    Gracefully shut down the LSS service.
    - Closes all WebSocket connections.
    - Cancels background tasks.
    """
    global stop_flag, update_task

    api_logger.info("Shutting down LSS service...")

    # Stop live updates
    stop_flag = True
    if update_task:
        api_logger.info("Cancelling live updates task...")
        update_task.cancel()
        try:
            await update_task
        except asyncio.CancelledError:
            api_logger.info("Live updates task cancelled.")

    # Close all active WebSocket connections
    api_logger.info(f"Closing {len(active_connections)} active WebSocket connections...")
    for connection in active_connections:
        try:
            await connection.close()
        except Exception as e:
            api_logger.error(f"Failed to close WebSocket connection: {e}")
    active_connections.clear()

    api_logger.info("LSS shutdown complete.")        