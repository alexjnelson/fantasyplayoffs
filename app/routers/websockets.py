from fastapi import APIRouter
from typing import Optional
from enums.live_update_command import LiveUpdateCommand
import websockets
import asyncio
import logging

router = APIRouter(prefix="/lss")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main-service-websocket")

# Global variables
websocket_connection: Optional[websockets.WebSocketClientProtocol] = None
receive_task = None  # Reference to the live update task
stop_flag = False  # Flag to control live update reception

recv_lock = asyncio.Lock() 
reconnection_task: Optional[asyncio.Task] = None  # Task to manage the reconnection loop
shutdown_event = asyncio.Event()  # Used to signal application shutdown

@router.on_event("startup")
async def start_reconnection_loop():
    """
    Start the reconnection loop when the app starts.
    """
    global reconnection_task

    # Start the reconnection loop as a background task
    reconnection_task = asyncio.create_task(reconnection_loop())

async def reconnection_loop():
    """
    Loop to manage WebSocket reconnection attempts.
    Terminates when the shutdown event is set.
    """
    global websocket_connection

    uri = "ws://localhost:8080/ws/football"  # WebSocket URL

    while not shutdown_event.is_set():
        try:
            logger.info("Attempting to connect to LSS WebSocket...")
            websocket_connection = await asyncio.wait_for(websockets.connect(uri), timeout=5)
            logger.info("WebSocket connection established.")
            return  # Exit loop on successful connection
        except asyncio.TimeoutError:
            logger.warning("Connection attempt timed out.")
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
        logger.info("Retrying in 5 seconds...")
        await asyncio.sleep(5)  # Retry after delay

    logger.info("Shutdown event set. Exiting reconnection loop.")


@router.post("/start")
async def start_live_updates():
    """
    Start receiving live updates from the WebSocket server.
    """
    global websocket_connection, receive_task, stop_flag

    if not websocket_connection:
        return {"error": "WebSocket connection not established."}

    if receive_task and not receive_task.done():
        return {"error": "Live updates are already running."}

    try:
        # Protect the send and receive with a lock
        async with recv_lock:
            await websocket_connection.send(LiveUpdateCommand.START)
            response = await websocket_connection.recv()
            logger.info(f"Response from LSS: {response}")

        stop_flag = False
        receive_task = asyncio.create_task(receive_live_updates())
        return {"message": "Live updates started."}
    except Exception as e:
        logger.error(f"Failed to start live updates: {e}")
        return {"error": str(e)}


@router.post("/stop")
async def stop_live_updates():
    """
    Stop receiving live updates from the WebSocket server.
    """
    global websocket_connection, receive_task, stop_flag

    if not websocket_connection:
        return {"error": "WebSocket connection not established."}

    if receive_task is None or receive_task.done():
        return {"error": "Live updates are not running."}

    try:
        # Protect the send and receive with a lock
        async with recv_lock:
            await websocket_connection.send(LiveUpdateCommand.STOP)
            response = await websocket_connection.recv()
            logger.info(f"Response from LSS: {response}")

        # Signal the background task to stop
        stop_flag = True
        await receive_task  # Wait for the task to finish
        logger.info("Live updates stopped.")
        return {"message": "Live updates stopped."}
    except Exception as e:
        logger.error(f"Failed to stop live updates: {e}")
        return {"error": str(e)}


async def receive_live_updates():
    """
    Task to receive live updates from the WebSocket server.
    Includes reconnection logic and uses a lock to prevent concurrent recv calls.
    """
    global stop_flag, websocket_connection, recv_lock

    while not stop_flag:
        try:
            async with recv_lock:  # Ensure only one coroutine can call recv
                if websocket_connection is None:
                    logger.warning("WebSocket connection lost. Reconnecting...")
                    await connect_websocket()  # Attempt reconnection

                data = await websocket_connection.recv()  # Receive data
                logger.info(f"Received Data: {data}")
        except websockets.exceptions.ConnectionClosedError as e:
            logger.warning(f"WebSocket connection closed: {e}")
            websocket_connection = None
        except Exception as e:
            logger.error(f"Error during live updates: {e}")
            await asyncio.sleep(5)

    logger.info("Receive live updates task has exited.")


@router.on_event("shutdown")
async def shutdown_websocket():
    """
    Gracefully close the WebSocket connection during shutdown.
    """
    global websocket_connection, reconnection_task

    logger.info("Shutting down WebSocket client...")

    # Signal the reconnection loop to stop
    shutdown_event.set()

    # Cancel the reconnection loop
    if reconnection_task:
        logger.info("Cancelling reconnection loop...")
        reconnection_task.cancel()
        try:
            await reconnection_task
        except asyncio.CancelledError:
            pass

    # Close the WebSocket connection if it's open
    if websocket_connection:
        logger.info("Closing WebSocket connection...")
        try:
            await websocket_connection.close()
        except Exception as e:
            logger.error(f"Error closing WebSocket: {e}")

    logger.info("WebSocket client shutdown complete.")