from fastapi import APIRouter, WebSocket
from typing import Optional
import websockets
import asyncio
import logging

router = APIRouter(prefix="/lss")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main-service-websocket")

# List to keep track of active WebSocket clients
websocket_connection: Optional[websockets.WebSocketClientProtocol] = None
stop_flag = False  # Flag to control live update loop
receive_task = None  # Reference to the task that processes live updates



@router.on_event("startup")
async def connect_websocket():
    """
    Establish the WebSocket connection on app startup.
    """
    global websocket_connection
    uri = "ws://localhost:8080/ws/football"  # WebSocket URL
    while websocket_connection is None:  # Attempt to connect until successful
        try:
            websocket_connection = await websockets.connect(uri)
            logger.info("WebSocket connection established.")
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
            logger.info("Retrying in 5 seconds...")
            await asyncio.sleep(5)  # Retry after 5 seconds


@router.post("/start")
async def start_receiving_updates():
    """
    Start receiving live updates from the WebSocket server.
    """
    global stop_flag, receive_task
    if not websocket_connection:
        return {"error": "WebSocket connection not established."}

    if receive_task and not receive_task.done():
        return {"error": "Already receiving live updates."}

    stop_flag = False  # Reset the stop flag

    # Create a background task to handle receiving updates
    receive_task = asyncio.create_task(receive_live_updates())
    logger.info("Started receiving live updates.")
    return {"message": "Receiving live updates started."}


@router.post("/stop")
async def stop_receiving_updates():
    """
    Stop receiving live updates.
    """
    global stop_flag, receive_task
    if not receive_task or receive_task.done():
        return {"error": "No active update receiving task to stop."}

    stop_flag = True  # Set the stop flag
    await receive_task  # Wait for the task to finish
    logger.info("Stopped receiving live updates.")
    return {"message": "Receiving live updates stopped."}


async def receive_live_updates():
    """
    Task to receive live updates from the WebSocket server.
    Includes reconnection logic.
    """
    global stop_flag, websocket_connection

    while not stop_flag:
        try:
            if websocket_connection is None or websocket_connection.closed:
                logger.warning("WebSocket connection lost. Reconnecting...")
                await connect_websocket()  # Attempt reconnection

            data = await websocket_connection.recv()  # Receive data
            logger.info(f"Received Data: {data}")
        except websockets.exceptions.ConnectionClosedError as e:
            logger.warning(f"WebSocket connection closed: {e}")
            websocket_connection = None  # Mark connection as closed
        except Exception as e:
            logger.error(f"Error during live updates: {e}")
            await asyncio.sleep(5)  # Avoid tight reconnection loops

@router.on_event("shutdown")
async def close_websocket():
    """
    Close the WebSocket connection on app shutdown.
    """
    global websocket_connection
    if websocket_connection:
        await websocket_connection.close()
        logger.info("WebSocket connection closed.")
        websocket_connection = None
