from fastapi import HTTPException, requests, status
from jose import JWTError
from sqlmodel import Session
from app.config import Settings
from app.models import User


from app.config import Settings
from app.models import User


def decode_google_token(id_token: str) -> dict[str, any]:
    try:
        # Google's public keys URL
        certs_url = "https://www.googleapis.com/oauth2/v1/certs"
        response = requests.get(certs_url)
        certs = response.json()

        payload = jwt.decode(
            id_token,
            certs,
            algorithms=["RS256"],
            audience=Settings.CLIENT_ID,
            options={"verify_at_hash": False}
        )
        return payload
    except JWTError as e:
        raise JWTError("Token validation failed") from e


def authenticate_token(db: Session, code: str) -> User:
        # Exchange code for token
    token_response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": Settings.CLIENT_ID,
            "client_secret": Settings.CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": Settings.REDIRECT_URI,
        },
    ).json()

    # Extract ID token and access token from the response
    id_token = token_response.get("id_token")

    # Decode ID token to fetch user information
    try:
        payload = decode_google_token(id_token)
        google_id = payload.get("sub")
        user_email = payload.get("email")
        user_name = payload.get("name")
