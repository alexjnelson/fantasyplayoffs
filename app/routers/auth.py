from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from config import settings
from db import get_session
from models import Users
from services import get_or_create_user, get_user_by_email, get_token, authenticate_token


router = APIRouter(prefix="/auth")

@router.get("/login")
def login_route():
    if settings.ENVIRONMENT != "prod":
        raise HTTPException(403, "Login disabled on dev environment")
    
    scope = "openid email profile"
    return RedirectResponse(
        url=f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"response_type=code"
            f"&client_id={settings.CLIENT_ID}"
            f"&redirect_uri={settings.REDIRECT_URI}"
            f"&scope={scope}"
    )


@router.get("/callback")
async def auth_callback_route(code: str = None, db: Session = Depends(get_session)):
    if settings.ENVIRONMENT != "prod":
        raise HTTPException(403, "Login disabled on dev environment")
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Missing authorization code")
    
    id_token = get_token(code)
    user = authenticate_token(id_token)
    user = get_or_create_user(db, user)

    # Return the token(s) to the client
    return {
        "message": "User authenticated successfully",
        "id_token": id_token,
        "google_id": user.id,
        "email": user.email
    }


@router.post("/login-sso")
async def sso_login_route(id_token: str = Body(...), db: Session = Depends(get_session)):
    if settings.ENVIRONMENT != "prod":
        raise HTTPException(403, "Login disabled on dev environment")

    user = authenticate_token(id_token)
    user = get_or_create_user(db, user)

    return {
        "message": "User authenticated successfully",
        "google_id": user.id,
    }


@router.post("/dev-login")
async def dev_login_route(email: str = Body(...), db: Session = Depends(get_session)):
    if settings.ENVIRONMENT != "dev":
        raise HTTPException(403, "Dev login disabled on prod environment")

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(404, "User not found")
    
    return {
        "message": "User authenticated successfully",
        "google_id": user.id,
    }

    
@router.post("/dev-create-user")
async def dev_create_user_route(email: str = Body(...), name: str = Body(...), db: Session = Depends(get_session)):
    if settings.ENVIRONMENT != "dev":
        raise HTTPException(403, "Dev login disabled on prod environment")

    user = Users(
        id=email,
        name=name,
        email=email
    )
    
    user = get_or_create_user(db, user)
    return {
        "message": "User authenticated successfully",
        "google_id": user.id,
    }
