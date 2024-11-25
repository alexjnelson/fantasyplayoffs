import requests
from fastapi import HTTPException, status
from jose import JWTError, jwt

from config import settings
from models import Users


from jose.exceptions import JWTError

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
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error decoding token headers: {str(e)}"
            )

        # Validate the key ID (kid)
        kid = unverified_header.get("kid")
        if not kid or kid not in {key["kid"] for key in jwks["keys"]}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
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
