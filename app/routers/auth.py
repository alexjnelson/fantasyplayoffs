from fastapi import APIRouter, Depends, HTTPException, requests, status
from fastapi.responses import RedirectResponse
from jose import JWTError
from sqlmodel import Session
from app.config import Settings
from app.models import User
from app.db import get_session
from app.services import auth
from app.services.user import create_user, get_user


router = APIRouter(prefix="/auth")

@router.get("login")
def login_route():
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
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Missing authorization code")
    
    try:
        user = auth.authenticate_user(db, code)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


    # Check if user exists, if not create a new user
    user_ref = db.collection('users').document(google_id)
    user_doc = user_ref.get()
    if not user_doc.exists:
        user_data = {"email": user_email, "name": user_name}
        user_ref.set(user_data)

    # Return the token(s) to the client
    return {
        "message": "User authenticated successfully",
        "id_token": id_token,
        "google_id": google_id,
        "email": user_email
    }



@router.post("google-signin")
async def google_signin_route(id_token: str = Body(...)):
    try:
        # Decode ID token to fetch user information
        payload = decode_google_token(id_token)
        google_id = payload.get("sub")
        user_email = payload.get("email")
        user_name = payload.get("name")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    # Check if user exists, if not create a new user
    user_ref = db.collection('users').document(google_id)
    user_doc = user_ref.get()
    if not user_doc.exists:
        user_data = {"email": user_email, "name": user_name}
        user_ref.set(user_data)

    return {"message": "User signed in successfully", "google_id": google_id}

@router.post("/users/", response_model=User)
def create_user_route(user: User, session: Session = Depends(get_session)):
    user = create_user(session, user)
    return user
