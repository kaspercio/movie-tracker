from passlib.context import CryptContext
from jose import jwt
from time import time
import os
from dotenv import load_dotenv

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# jwt info
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE = os.getenv("ACCESS_TOKEN_EXPIRE")

def hash_password(password: str) -> str:
    hashed = pwd_context.hash(password)
    return hashed

def verify_password(user_password: str, hashed_password: str) -> bool:
    is_verified = pwd_context.verify(user_password, hashed_password)
    return is_verified

def create_token(user_id: int, user_name: str) -> str:
    payload = {
        "sub": str(user_id),
        "name": user_name, 
        "iat": time(),
        "exp": time() + int(ACCESS_TOKEN_EXPIRE)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict:
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_payload



