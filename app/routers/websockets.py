from fastapi import APIRouter, WebSocket
from typing import List
import websockets
import asyncio

import websockets.connection

router = APIRouter(prefix="/lss")

# List to keep track of connected WebSocket clients
connected_clients: List[WebSocket] = []

@router.post("/connect-websocket")
async def connect_websocket():
    uri = "ws://localhost:8080/ws"  # WebSocket URL of the FastAPI service inside Docker
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from LSS!")
        response = await websocket.recv()
        return {"message": response}
    
@router.post("/start")
async def receive_live_updates(): 
    uri =  'ws://localhost:8080/ws/football'
    async with websockets.connect(uri) as websocket:
        count = 0 
        flag = True
        while flag:
            try:
                data = await websocket.recv()
                count += 1
                if count < 20:
                    print(f"Received Data : {data}")
                else:
                    flag = False
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed") 
    
