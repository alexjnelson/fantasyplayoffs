from fastapi import FastAPI
from routers import auth_router
from routers.websockets import router as websocket_router
# Initialize FastAPI
app = FastAPI()

# Create database tables
@app.on_event("startup")
def on_startup():
    pass

# Include routers
app.include_router(auth_router, prefix="/api", tags=["User"])
app.include_router(websocket_router, prefix="/ws", tags=["WebSockets"])
