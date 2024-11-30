import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from alembic import command
from alembic.config import Config

from routers import auth_router
from config import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, tags=["Auth"])


@app.on_event("startup")
def on_startup():
    apply_migrations()


def apply_migrations():
    try:
        logger.info("Applying database migrations")

        # Run the Alembic upgrade command using subprocess
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Alembic upgrade failed: {result.stderr}")
            raise RuntimeError(f"Alembic upgrade failed: {result.stderr}")
        
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise
