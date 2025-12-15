from fastapi import FastAPI, APIRouter, Depends, HTTPException
import app.auth
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models import User
import schemas


router = APIRouter()

@router.get("/")
async def root():
    print("Welcome to the homepage.")

@router.post("/login")
async def login(credentials : schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if user:
        if app.auth.verify_password(credentials.password, user.hashed_password):
            new_token = app.auth.create_token(user.id, user.username)
            return new_token
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")