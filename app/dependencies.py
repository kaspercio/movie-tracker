from fastapi import HTTPException, Header
from jose import JWTError
from app.auth import verify_token

def get_current_user(authorization: str = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        token = authorization.split("Bearer ")[1]
        payload = verify_token(token)
        return payload
    except (IndexError, KeyError, JWTError):
        raise HTTPException(status_code=401, detail="Invalid token")