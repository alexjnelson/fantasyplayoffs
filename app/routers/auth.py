from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.config import Settings
from app.db import get_session
from app.models import User
from app.services import auth_service, users_service


router = APIRouter(prefix="/auth")

@router.get("login")
def login_route():
    if Settings.ENVIRONMENT != "prod":
        raise HTTPException(403, "Login disabled on dev environment")
    
    scope = "openid email profile"
    return RedirectResponse(
        url=f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"response_type=code"
            f"&client_id={Settings.CLIENT_ID}"
            f"&redirect_uri={Settings.REDIRECT_URI}"
            f"&scope={scope}"
    )


@router.get("callback")
async def auth_callback_route(code: str = None, db: Session = Depends(get_session)):
    if Settings.ENVIRONMENT != "prod":
        raise HTTPException(403, "Login disabled on dev environment")
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Missing authorization code")
    
    id_token = auth_service.get_token(code)
    user = auth_service.authenticate_token(id_token)
    user = users_service.get_or_create_user(db, user)

    # Return the token(s) to the client
    return {
        "message": "User authenticated successfully",
        "id_token": id_token,
        "google_id": user.id,
        "email": user.email
    }


@router.post("login-sso")
async def sso_login_route(id_token: str = Body(...), db: Session = Depends(get_session)):
    if Settings.ENVIRONMENT != "prod":
        raise HTTPException(403, "Login disabled on dev environment")

    user = auth_service.authenticate_token(id_token)
    user = users_service.get_or_create_user(db, user)

    return {
        "message": "User authenticated successfully",
        "google_id": user.id,
    }


@router.post("login-dev")
async def dev_login_route(email: str = Body(...), db: Session = Depends(get_session)):
    if Settings.ENVIRONMENT == "prod":
        raise HTTPException(403, "Dev login disabled on test environment")

    user = users_service.get_user_by_email(db, email)
    return {
        "message": "User authenticated successfully",
        "google_id": user.id,
    }

    
@router.post("login-dev")
async def dev_create_user_route(email: str = Body(...), name: str = Body(...), db: Session = Depends(get_session)):
    if Settings.ENVIRONMENT == "prod":
        raise HTTPException(403, "Dev login disabled on test environment")

    user = User(
        id=f"test_id_{email}",
        name=name,
        email=email
    )
    
    user = users_service.get_or_create_user(db, user)
    return {
        "message": "User authenticated successfully",
        "google_id": user.id,
    }
