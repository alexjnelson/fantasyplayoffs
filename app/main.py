from fastapi import FastAPI
from app.routers import user
from app.db import engine
from app.models import SQLModel

# Initialize FastAPI
app = FastAPI()

# Create database tables
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Include routers
app.include_router(user.router, prefix="/api", tags=["User"])
