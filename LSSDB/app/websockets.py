from fastapi import APIRouter
import asyncio
import logging
from fastapi import WebSocket, WebSocketDisconnect
from app.config.logging_config import setup_logging
from app.enums.live_update_command import LiveUpdateCommand
from app.utils.mock_data_generator import generate_mock_data

router = APIRouter(prefix="/websockets")

# Set up logging
setup_logging()
api_logger = logging.getLogger("api")
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")


## WEBSOCKET ENDPOINTS ##
send_updates_event = asyncio.Event()  # Event to control live updates
tasks = {}  # Dictionary to track tasks for each connection


active_connections = []

@router.websocket("/ws/football")
async def live_data_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for live football updates.
    Responds to start/stop commands and sends live updates.
    """
    await websocket.accept()
    active_connections[websocket] = None  # Track task for each connection
    api_logger.info(f"New WebSocket connection established: {websocket.client}")

    try:
        while True:
            # Wait for a command from the client
            command = await websocket.receive_text()
            api_logger.info(f"Received command: {command}")

            if command.lower() == LiveUpdateCommand.START:
                await handle_start_command(websocket)
            elif command.lower() == LiveUpdateCommand.STOP:
                await handle_stop_command(websocket)
            else:
                api_logger.warning(f"Unknown command received: {command}")
                await websocket.send_text("Invalid command. Use START or STOP.")
    except WebSocketDisconnect:
        await handle_disconnect(websocket)
    except Exception as e:
        api_logger.error(f"Error in WebSocket connection with {websocket.client}: {e}")
    finally:
        await handle_disconnect(websocket)


async def handle_start_command(websocket: WebSocket):
    """
    Handle the START command to initiate live updates for a client.
    """
    # if websocket in active_connections and active_connections[websocket] and not active_connections[websocket].done():
    #     await websocket.send_text("Live updates already running.")
    #     api_logger.info(f"START command ignored: updates already running for {websocket.client}")
    #     return

    # Start live updates for this client
    send_updates_event.set()  # Enable global updates
    active_connections[websocket] = asyncio.create_task(send_live_updates(websocket))
    api_logger.info(f"Live updates started for client: {websocket.client}")
    await websocket.send_text("Live updates started.")


async def handle_stop_command(websocket: WebSocket):
    """
    Handle the STOP command to terminate live updates for a client.
    """
    if not active_connections[websocket] or active_connections[websocket].done():
        await websocket.send_text("Live updates are not running.")
        api_logger.info(f"STOP command ignored: no active updates for {websocket.client}")
        return

    # Stop live updates for this client
    active_connections[websocket].cancel()
    try:
        await active_connections[websocket]  # Wait for the task to finish
    except asyncio.CancelledError:
        api_logger.info(f"Live updates task cancelled for client: {websocket.client}")

    active_connections[websocket] = None  # Clear the task
    api_logger.info(f"Live updates stopped for client: {websocket.client}")
    await websocket.send_text("Live updates stopped.")


async def handle_disconnect(websocket: WebSocket):
    """
    Handle cleanup when a client disconnects.
    """
    if websocket in active_connections:
        if active_connections[websocket]:
            active_connections[websocket].cancel()
            try:
                await active_connections[websocket]  # Wait for task cancellation
            except asyncio.CancelledError:
                api_logger.info(f"Task cancelled for disconnected client: {websocket.client}")
        del active_connections[websocket]
    api_logger.info(f"Client disconnected: {websocket.client}")


async def send_live_updates(websocket: WebSocket):
    """
    Send live updates to a single WebSocket client while updates are enabled.
    """
    try:
        while send_updates_event.is_set():
            mock_data = generate_mock_data()
            await websocket.send_json(mock_data)
            api_logger.info(f"Sent live update to client {websocket.client}: {mock_data}")
            await asyncio.sleep(5)  # Simulate delay between updates
    except asyncio.CancelledError:
        api_logger.info(f"Live updates stopped for client: {websocket.client}")
    except Exception as e:
        api_logger.error(f"Error sending live update to client {websocket.client}: {e}")


@router.on_event("shutdown")
async def shutdown():
    """
    Gracefully shut down the LSS service.
    - Closes all WebSocket connections.
    """
    api_logger.info(f"Shutting down LSS service... Closing {len(active_connections)} active connections.")
    for websocket, task in active_connections.items():
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                api_logger.info(f"Task cancelled for client: {websocket.client}")
        try:
            await websocket.close()
        except Exception as e:
            api_logger.error(f"Failed to close WebSocket connection: {e}")
    active_connections.clear()
    api_logger.info("LSS shutdown complete.")
