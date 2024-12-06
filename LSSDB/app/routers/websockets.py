from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import logging
from app.config.logging_config import setup_logging
from app.enums.live_update_command import LiveUpdateCommand
from app.utils.mock_data_generator import generate_mock_data

router = APIRouter(prefix="/ws")

# Set up logging
setup_logging()
api_logger = logging.getLogger("api")

# Track active connections and tasks
active_connections = {}  # {websocket: task}
send_updates_event = asyncio.Event()  # Control live updates


@router.websocket("/live_data")
async def live_data_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for live football updates.
    Responds to START and STOP commands and manages live updates.
    """
    
    await websocket.accept()
    active_connections[websocket] = None  # Track the WebSocket connection
    api_logger.info(f"New WebSocket connection established: {websocket.client}")

    try:
        while True:
            command = await websocket.receive_text()
            api_logger.info(f"Received command: {command}")

            if command.lower() == LiveUpdateCommand.START:
                await handle_start_command(websocket)
            elif command.lower() == LiveUpdateCommand.STOP:
                await handle_stop_command(websocket)
            else:
                await websocket.send_text("Invalid command. Use START or STOP.")
    except WebSocketDisconnect:
        api_logger.info(f"Client disconnected: {websocket.client}")
        await handle_disconnect(websocket)
    except Exception as e:
        api_logger.error(f"Error in WebSocket connection: {e}")
    finally:
        await handle_disconnect(websocket)


async def handle_start_command(websocket: WebSocket):
    """
    Handle the START command to initiate live updates for a client.
    """
    
    task = active_connections.get(websocket)
    api_logger.info(f"Handling START command for {websocket.client}")

    # Ensure no existing task is running
    if task and not task.done():
        await websocket.send_text("Live updates already running.")
        api_logger.info("START command ignored: updates already running.")
        return

    # Clear any old tasks
    if task and task.done():
        active_connections[websocket] = None
        api_logger.info(f"Cleared old task for {websocket.client}")

    # Reset event and start a new task
    send_updates_event.set()
    active_connections[websocket] = asyncio.create_task(send_live_updates(websocket))

    await websocket.send_text("Live updates started.")
    api_logger.info("Live updates started.")


async def handle_stop_command(websocket: WebSocket):
    """
    Handle the STOP command to terminate live updates for a client.
    """
    # Debugging: Log current task state
    task = active_connections.get(websocket)
    api_logger.info(f"Handling STOP command for {websocket.client}")

    # Ensure a task exists and is running
    if not task or task.done():
        await websocket.send_text("Live updates are not running.")
        api_logger.info("STOP command ignored: no active updates.")
        return

    # Stop live updates
    send_updates_event.clear()
    task.cancel()  # Cancel the running task
    try:
        await task  # Wait for task completion
    except asyncio.CancelledError:
        api_logger.info("Live updates task cancelled.")

    # Clear the task reference
    active_connections[websocket] = None
    api_logger.info(f"Cleared task for {websocket.client}")
    await websocket.send_text("Live updates stopped.")
    api_logger.info("Live updates stopped.")



async def handle_disconnect(websocket: WebSocket):
    """
    Handle cleanup when a client disconnects.
    """
    if websocket in active_connections:
        if active_connections[websocket]:
            active_connections[websocket].cancel()
            try:
                await active_connections[websocket]
            except asyncio.CancelledError:
                pass
        del active_connections[websocket]
    api_logger.info(f"Cleaned up for client: {websocket.client}")


async def send_live_updates(websocket: WebSocket):
    """
    Send live updates to a single WebSocket client while updates are enabled.
    """
    try:
        while send_updates_event.is_set():
            mock_data = generate_mock_data()
            await websocket.send_json(mock_data)
            api_logger.info(f"Sent live update to client: {mock_data}")
            await asyncio.sleep(5)  # Simulate update frequency
    except asyncio.CancelledError:
        api_logger.info("Live updates task cancelled.")
    except Exception as e:
        api_logger.error(f"Error sending live update: {e}")


@router.on_event("shutdown")
async def shutdown():
    """
    Shut down the service gracefully by cleaning up tasks and connections.
    """
    api_logger.info(f"Shutting down LSS service with {len(active_connections)} connections.")
    for websocket, task in list(active_connections.items()):
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        try:
            await websocket.close()
        except Exception as e:
            api_logger.error(f"Error closing WebSocket: {e}")
    active_connections.clear()
    api_logger.info("LSS service shutdown complete.")
