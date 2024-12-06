from fastapi.security import APIKeyHeader
import requests
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from jose.exceptions import JWTError
from sqlmodel import Session

from db import get_session
from services.users import get_user, get_user_by_email
from config import settings
from models import Users


api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def decode_google_token(id_token: str) -> dict[str, any]:
    try:
        # Get Google public certs
        certs_url = "https://www.googleapis.com/oauth2/v3/certs"
        response = requests.get(certs_url)
        jwks = response.json()

        # Extract headers
        try:
            unverified_header = jwt.get_unverified_header(id_token)
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Error decoding token headers: {str(e)}"
            )

        # Validate the key ID (kid)
        kid = unverified_header.get("kid")
        if not kid or kid not in {key["kid"] for key in jwks["keys"]}:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find appropriate key for token"
            )

        # Find the correct key
        key = next(key for key in jwks["keys"] if key["kid"] == kid)

        # Verify and decode the token
        payload = jwt.decode(
            id_token,
            key,
            algorithms=["RS256"],
            audience=settings.CLIENT_ID,
            options={"verify_at_hash": False},
        )

        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid token: {str(e)}"
        )
    
def get_token(code: str) -> str:
    # Exchange code for token
    token_response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.REDIRECT_URI,
        },
    ).json()

    # Extract ID token and access token from the response
    return token_response.get("id_token")


def authenticate_token(id_token: str) -> Users:        
    payload = decode_google_token(id_token)
    return Users(
        id=payload.get("sub"),
        name=payload.get("name"),
        email=payload.get("email")
    )


def extract_token(authorization: str = Depends(api_key_header)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    try:
        scheme, value = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization scheme must be Bearer"
            )
        return value
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format"
        )


def validate_user(authorization: str = Depends(extract_token), db: Session = Depends(get_session)):
    if settings.ENVIRONMENT == "dev":
        user = get_user_by_email(db, authorization)
    else:
        user = authenticate_token(authorization)
        user = get_user(user.id)

    if user is not None:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

