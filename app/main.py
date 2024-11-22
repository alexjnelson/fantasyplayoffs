from fastapi import FastAPI
from routers import auth_router

# Initialize FastAPI
app = FastAPI()

# Create database tables
@app.on_event("startup")
def on_startup():
    pass

# Include routers
app.include_router(auth_router, prefix="/api", tags=["User"])
