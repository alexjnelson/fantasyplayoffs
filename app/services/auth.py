from fastapi import HTTPException, requests, status
from jose import JWTError, jwt

from config import settings
from models import Users


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
            audience=settings.CLIENT_ID,
            options={"verify_at_hash": False}
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


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
