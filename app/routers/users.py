from fastapi import APIRouter, Depends, HTTPException
import app.auth
import re
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import LoginRequest, RegisterRequest


router = APIRouter()

@router.post("/login")
async def login(credentials : LoginRequest, db: Session = Depends(get_db)):
    # look up username in db if it exists
    user = db.query(User).filter(User.username == credentials.username).first()
    if user:
        # compare the entered password is the same as hashed
        if app.auth.verify_password(credentials.password, user.hashed_password):
            # create a jwt
            new_token = app.auth.create_token(user.id, user.username)
            return new_token
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@router.post("/register")
async def register(credentials: RegisterRequest, db: Session = Depends(get_db)):
    # check all failure conditions first
    if credentials.password != credentials.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")
    
    if not app.auth.validate_password(credentials.password):
        raise HTTPException(status_code=400, detail="Password doesn't meet criteria")
    
    email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    if not re.fullmatch(email_regex, credentials.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    user = db.query(User).filter(User.username == credentials.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    email_exists = db.query(User).filter(User.email == credentials.email).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # if we get here, create the user
    hashed_password = app.auth.hash_password(credentials.password)
    new_user = User(
        username=credentials.username,
        email=credentials.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": f"Account created for {credentials.username}"}

@router.get("/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user["sub"],
        "username": current_user["name"]
    }