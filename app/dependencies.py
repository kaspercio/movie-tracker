from fastapi import HTTPException, Depends
from jose import JWTError
from app.auth import verify_token
from app.database import SessionLocal
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

# fastAPI depends function to check token validity
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    try:
        payload = verify_token(token)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()