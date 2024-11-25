from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth_router
from config import settings


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/api", tags=["User"])


@app.on_event("startup")
def on_startup():
    pass

