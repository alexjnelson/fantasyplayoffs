from fastapi import APIRouter
from typing import Optional
import websockets
import asyncio
import logging
from enums.live_update_command import LiveUpdateCommand

router = APIRouter(prefix="/lss")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main-service-websocket")

# Global variables
websocket_connection: Optional[websockets.WebSocketClientProtocol] = None
receive_task: Optional[asyncio.Task] = None  # Task for receiving updates
stop_flag = False  # Flag to control live update reception
recv_lock = asyncio.Lock()  # Prevent concurrent recv calls
reconnection_task: Optional[asyncio.Task] = None  # Task to manage reconnections
shutdown_event = asyncio.Event()  # Event to signal shutdown


@router.on_event("startup")
async def start_reconnection_loop():
    """
    Start the reconnection loop when the app starts.
    """
    global reconnection_task

    # Start the reconnection loop as a background task
    reconnection_task = asyncio.create_task(reconnection_loop())


connection_lock = asyncio.Lock()

async def reconnection_loop():
    global websocket_connection

    uri = "ws://localhost:8080/websockets/ws/live_data"

    async with connection_lock:
        if websocket_connection:
            logger.info("WebSocket connection already exists. Skipping reconnection.")
            return
        while not shutdown_event.is_set():
            try:
                logger.info("Attempting to connect to LSS WebSocket...")
                websocket_connection = await websockets.connect(uri)
                logger.info("WebSocket connection established.")
                break
            except Exception as e:
                logger.error(f"Failed to connect to WebSocket: {e}")
                logger.info("Retrying in 5 seconds...")
                await asyncio.sleep(5)  # Retry after delay


@router.post("/start")
async def start_live_updates():
    """
    Start receiving live updates from the WebSocket server.
    """
    global websocket_connection, receive_task, stop_flag

    # Ensure connection is valid
    if not websocket_connection:
        logger.warning("WebSocket connection is closed. Reconnecting...")
        await reconnection_loop()
        if not websocket_connection:
            return {"error": "Failed to establish WebSocket connection."}

    # Prevent duplicate tasks
    if receive_task and not receive_task.done():
        return {"error": "Live updates are already running."}

    try:
        # Send START command
        async with recv_lock:
            await websocket_connection.send(LiveUpdateCommand.START)
            response = await websocket_connection.recv()
            logger.info(f"Response from LSS: {response}")

        # Start receiving updates
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

    # Ensure connection is valid
    if not websocket_connection:
        return {"error": "WebSocket connection not established."}

    # Ensure task exists
    if not receive_task or receive_task.done():
        return {"error": "Live updates are not running."}

    try:
        # Send STOP command
        async with recv_lock:
            await websocket_connection.send(LiveUpdateCommand.STOP)
            response = await websocket_connection.recv()
            logger.info(f"Response from LSS: {response}")

        # Stop receiving updates
        stop_flag = True
        if receive_task:
            receive_task.cancel()
            try:
                await receive_task
            except asyncio.CancelledError:
                logger.info("Receive task cancelled.")
            receive_task = None
        logger.info("Live updates stopped.")
        return {"message": "Live updates stopped."}
    except Exception as e:
        logger.error(f"Failed to stop live updates: {e}")
        return {"error": str(e)}    

async def receive_live_updates():
    """
    Task to receive live updates from the WebSocket server.
    """
    global stop_flag, websocket_connection, recv_lock

    while not stop_flag:
        try:
            async with recv_lock:
                if not websocket_connection:
                    logger.warning("WebSocket connection lost. Reconnecting...")
                    await reconnection_loop()  # Attempt reconnection

                data = await websocket_connection.recv()
                logger.info(f"Received live update: {data}")
        except websockets.ConnectionClosedError as e:
            logger.warning(f"WebSocket connection closed: {e}")
            websocket_connection = None
        except Exception as e:
            logger.error(f"Error receiving updates: {e}")
            await asyncio.sleep(5)  # Avoid tight reconnection loops

    logger.info("Receive updates task exited.")


@router.on_event("shutdown")
async def shutdown_websocket():
    """
    Gracefully close WebSocket and cancel tasks during shutdown.
    """
    global websocket_connection, reconnection_task

    logger.info("Shutting down WebSocket client...")

    # Signal shutdown
    shutdown_event.set()

    # Cancel reconnection loop
    if reconnection_task:
        logger.info("Cancelling reconnection loop...")
        reconnection_task.cancel()
        try:
            await reconnection_task
        except asyncio.CancelledError:
            pass

    # Close WebSocket connection
    if websocket_connection:
        logger.info("Closing WebSocket connection...")
        try:
            await websocket_connection.close()
        except Exception as e:
            logger.error(f"Error closing WebSocket: {e}")

    logger.info("WebSocket client shutdown complete.")
