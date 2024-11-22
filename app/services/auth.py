from fastapi import HTTPException, requests, status
from jose import JWTError, jwt
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
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


def authenticate_token(id_token: str) -> User:        
    payload = decode_google_token(id_token)
    return User(
        id=payload.get("sub"),
        name=payload.get("name"),
        email=payload.get("email")
    )


def get_token(code: str) -> str:
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
    return token_response.get("id_token")