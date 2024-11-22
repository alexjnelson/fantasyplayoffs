from fastapi import FastAPI
from app.routers import auth

# Initialize FastAPI
app = FastAPI()

# Create database tables
@app.on_event("startup")
def on_startup():
    pass

# Include routers
app.include_router(auth.router, prefix="/api", tags=["User"])
